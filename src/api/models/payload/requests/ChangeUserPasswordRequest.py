from pydantic import BaseModel

from src.api.typing.PasswordValidator import IsStrongPassword


class ChangeUserPasswordRequest(BaseModel):
    old_password: str
    new_password: IsStrongPassword
