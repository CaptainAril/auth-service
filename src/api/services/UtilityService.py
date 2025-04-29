import hmac
import hashlib
from uuid import uuid4
from typing import TypedDict
from datetime import UTC, datetime, timedelta

import jwt
import bcrypt
from faker import Faker
from django.utils import timezone
from ninja.errors import AuthenticationError

from src.env import jwt_config
from src.utils.svcs import Service
from src.utils.logger import Logger
from src.api.typing.JWT import JWTData
from src.api.models.postgres import User
from src.api.typing.ExpireUUID import ExpireUUID
from src.api.enums.CharacterCasing import CharacterCasing

DEFAULT_CHARACTER_LENGTH = 12
fake = Faker()


class SignatureData(TypedDict):
    title: str
    signature: str
    timestamp: str
    key: str
    ttl: int | float


@Service()
class UtilityService:
    @staticmethod
    async def hash_string(input: str) -> str:
        if not input:
            return ""

        salt: bytes = bcrypt.gensalt(10)
        hashed_string: bytes = bcrypt.hashpw(input.encode(), salt)

        return hashed_string.decode()

    @staticmethod
    async def compare_hash(input: str, hash: str) -> bool:
        is_same = bcrypt.checkpw(input.encode(), hash.encode())
        return is_same

    @staticmethod
    def generate_random_string(
        length: int = DEFAULT_CHARACTER_LENGTH,
        casing: CharacterCasing = CharacterCasing.LOWER,
        numeric_only: bool = False,
    ) -> str:
        if length <= 0:
            return ""

        if numeric_only:
            return str(fake.random_number(digits=length, fix_len=True))
        else:
            string_template = "".join(
                fake.random_elements(elements=("?", "#"), length=length)
            )
            string = fake.bothify(text=string_template)

            if casing == CharacterCasing.UPPER:
                return string.upper()
            elif casing == CharacterCasing.LOWER:
                return string.lower()
            else:
                return string

    @staticmethod
    def sanitize_user_object(user: User | None = None) -> User:  # type: ignore
        if user:
            del user.password

            return user

    @staticmethod
    def generate_jwt(email: str, user_uuid: str) -> str:
        jwt_data = {"email": email, "user_id": user_uuid}
        jwt_claims = {
            "exp": timezone.now() + timedelta(seconds=3600),
            "iss": jwt_config["issuer"],
            "aud": jwt_config["issuer"],
        }
        return jwt.encode(dict(jwt_data, **jwt_claims), jwt_config["secret"])

    @staticmethod
    def decrypt_jwt(token: str) -> JWTData | None:
        try:
            data = jwt.decode(
                token,
                jwt_config["secret"],
                algorithms=["HS256"],
                issuer=jwt_config["issuer"],
                audience=jwt_config["issuer"],
            )
            return {"email": data["email"], "user_id": data["user_id"]}
        except jwt.exceptions.InvalidTokenError:
            ...

    @staticmethod
    def generate_uuid() -> ExpireUUID:
        current_time = timezone.now()
        lifespan = timedelta(hours=24)
        expires_at = current_time + lifespan
        return {"uuid": uuid4(), "expires_at": expires_at}

    @staticmethod
    def generate_signature(key: str, timestamp: str) -> str:
        signature = hmac.new(
            key=key.encode(), msg=timestamp.encode(), digestmod=hashlib.sha256
        ).hexdigest()
        return signature

    @staticmethod
    def verify_signature(signature_data: SignatureData, logger: Logger) -> bool:
        signature = signature_data["signature"]
        timestamp = signature_data["timestamp"]
        key = signature_data["key"]
        ttl = signature_data["ttl"]
        title = signature_data["title"]

        valid_signature = UtilityService.generate_signature(key, timestamp)
        is_valid = hmac.compare_digest(valid_signature, signature)

        if not is_valid:
            message = "Invalid signature!"
            logger.error(
                {
                    "activity_type": f"Authenticate {title} Request",
                    "message": message,
                    "metadata": {"signature": signature},
                }
            )
            raise AuthenticationError(message=message)

        initial_time = datetime.fromtimestamp(float(timestamp), UTC)
        valid_window = initial_time + timedelta(minutes=ttl)
        if valid_window < datetime.now(UTC):
            message = "Signature expired!"
            logger.error(
                {
                    "activity_type": f"Authenticate {title} Request",
                    "message": message,
                    "metadata": {"timestamp": timestamp},
                }
            )
            raise AuthenticationError(message=message)

        return True

    @staticmethod
    def get_timestamp() -> str:
        current_time = datetime.now(UTC).timestamp()
        return str(current_time)
