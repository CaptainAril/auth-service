from typing import Annotated

from django.utils import timezone

from src.utils.svcs import Service
from src.utils.logger import Logger
from src.api.constants.messages import MESSAGES, DYNAMIC_MESSAGES
from src.api.typing.UserSuccess import UserSuccess
from src.api.constants.activity_types import ACTIVITY_TYPES
from src.api.repositories.UserRepository import UserRepository
from src.api.repositories.PasswordResetRepository import PasswordResetRepository
from src.api.models.payload.requests.PasswordResetRequest import (
    PasswordResetRequest,
    ConfirmPasswordResetRequest,
)

from .UtilityService import UtilityService


@Service()
class PasswordResetService:
    def __init__(
        self,
        logger: Annotated[Logger, "PasswordResetService"],
        utility_service: UtilityService,
    ) -> None:
        self.logger = logger
        self.utility_service = utility_service

    async def request_password_reset(self, req: PasswordResetRequest) -> UserSuccess:
        existing_user = await UserRepository.find_by_email(req.email)
        if not existing_user:
            self.logger.warn(
                {
                    "activity_type": ACTIVITY_TYPES["REQUEST_RESET_PASSWORD"],
                    "message": MESSAGES["USER"]["DOESNT_EXIST"],
                    "metadata": {"user": {"email": req.email}},
                }
            )
            return {
                "is_success": False,
                "message": MESSAGES["PASSWORD_RESET"]["DOESNT_EXIST"],
            }
        elif not existing_user.is_active:
            self.logger.info(
                {
                    "activity_type": ACTIVITY_TYPES["REQUEST_RESET_PASSWORD"],
                    "message": MESSAGES["PASSWORD_RESET"]["INACTIVE"],
                    "metadata": {"user": {"email": req.email}},
                }
            )
            return {
                "is_success": False,
                "message": MESSAGES["PASSWORD_RESET"]["INACTIVE"],
            }
        elif not existing_user.is_enabled:
            self.logger.info(
                {
                    "activity_type": ACTIVITY_TYPES["REQUEST_RESET_PASSWORD"],
                    "message": MESSAGES["PASSWORD_RESET"]["DISABLED"],
                    "metadata": {"user": {"email": req.email}},
                }
            )
            return {
                "is_success": False,
                "message": MESSAGES["PASSWORD_RESET"]["DISABLED"],
            }
        password_reset_token = self.utility_service.generate_uuid()
        uuid = password_reset_token["uuid"]
        expires_at = password_reset_token["expires_at"]
        await PasswordResetRepository.set_new_password_reset_token(
            existing_user, uuid, expires_at
        )

        self.logger.info(
            {
                "activity_type": ACTIVITY_TYPES["REQUEST_RESET_PASSWORD"],
                "message": DYNAMIC_MESSAGES["PASSWORD_RESET"]["EMAIL_SENT"](req.email),
                "metadata": {
                    "user": {"email": req.email},
                    "reset_token": existing_user.password_reset_token,
                },
            }
        )
        return {
            "is_success": True,
            "message": DYNAMIC_MESSAGES["PASSWORD_RESET"]["EMAIL_SENT"](req.email),
        }

    async def confirm_password_reset(
        self, req: ConfirmPasswordResetRequest
    ) -> UserSuccess:
        existing_user = await UserRepository.find_by_reset_token(req.reset_token)
        if not existing_user:
            self.logger.warn(
                {
                    "activity_type": "Confirm password reset",
                    "message": MESSAGES["USER"]["DOESNT_EXIST"],
                    "metadata": {"token": req.reset_token},
                }
            )
            return {
                "is_success": False,
                "message": "Invalid password reset token!",
            }
        elif not existing_user.is_active:
            self.logger.info(
                {
                    "activity_type": "Confirm password reset",
                    "message": MESSAGES["PASSWORD_RESET"]["INACTIVE"],
                    "metadata": {"token": req.reset_token},
                }
            )
            return {
                "is_success": False,
                "message": MESSAGES["PASSWORD_RESET"]["INACTIVE"],
            }
        elif not existing_user.is_enabled:
            self.logger.info(
                {
                    "activity_type": "Confirm password reset",
                    "message": MESSAGES["PASSWORD_RESET"]["DISABLED"],
                    "metadata": {"token": req.reset_token},
                }
            )
            return {
                "is_success": False,
                "message": MESSAGES["PASSWORD_RESET"]["DISABLED"],
            }

        if existing_user.token_expires_at < timezone.now():
            self.logger.warn(
                {
                    "activity_type": "Confirm password reset",
                    "message": MESSAGES["PASSWORD_RESET"]["TOKEN_EXPIRED"],
                    "metadata": {"token": req.reset_token},
                }
            )
            return {
                "is_success": False,
                "message": MESSAGES["PASSWORD_RESET"]["TOKEN_EXPIRED"],
            }
        new_password_hash = await self.utility_service.hash_string(req.new_password)
        await UserRepository.update_by_user(
            existing_user, {"password": new_password_hash}
        )
        message = MESSAGES["PASSWORD_RESET"]["PASSWORD_RESET"]
        self.logger.info(
            {
                "activity_type": "Confirm password reset",
                "message": message,
                "metadata": {"user": {"id": id}},
            }
        )

        return {"is_success": True, "message": message}
