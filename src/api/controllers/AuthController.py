from http import HTTPStatus
from typing import Annotated

from src.utils.svcs import Service
from src.utils.logger import Logger
from src.api.constants.messages import MESSAGES
from src.api.services.AuthService import AuthService
from src.api.utils.response_format import error_response, success_response
from src.api.models.payload.requests.ResendUserOtp import ResendUserOtp
from src.api.models.payload.requests.CreateUserRequest import CreateUserRequest
from src.api.models.payload.requests.AuthenticateUserOtp import AuthenticateUserOtp
from src.api.models.payload.requests.AuthenticateUserRequest import (
    AuthenticateUserRequest,
)
from src.api.models.payload.requests.ChangeUserPasswordRequest import (
    ChangeUserPasswordRequest,
)


@Service()
class AuthController:
    def __init__(
        self, logger: Annotated[Logger, "AuthController"], auth_service: AuthService
    ) -> None:
        self.logger = logger
        self.auth_service = auth_service

    async def register(self, user_data: CreateUserRequest) -> tuple:
        user_exists = await self.auth_service.register(user_data)
        if user_exists["is_exists"]:
            return error_response(
                user_exists["message"], status_code=HTTPStatus.BAD_REQUEST
            )
        return success_response(
            message=user_exists["message"],
            data=user_exists["user"],
            status_code=HTTPStatus.CREATED,
        )

    async def resend_email(self, credentials: ResendUserOtp) -> tuple:
        email_message = await self.auth_service.resend_email(credentials)
        if not email_message["is_success"]:
            return error_response(
                email_message["message"], status_code=HTTPStatus.BAD_REQUEST
            )
        return success_response(
            message=email_message["message"], status_code=HTTPStatus.OK
        )

    async def validate_email(self, credentials: AuthenticateUserOtp) -> tuple:
        is_valid = await self.auth_service.validate_email(credentials)
        if not is_valid:
            return error_response(
                MESSAGES["REGISTRATION"]["VERIFICATION_FAILED"],
                status_code=HTTPStatus.BAD_REQUEST,
            )
        return success_response(
            message=MESSAGES["REGISTRATION"]["VERIFICATION_SUCCESS"],
            status_code=HTTPStatus.OK,
        )

    async def login(self, credentials: AuthenticateUserRequest) -> tuple:
        auth_user = await self.auth_service.login(credentials)
        if not auth_user["is_success"]:
            return error_response(
                message=auth_user["message"], status_code=HTTPStatus.BAD_REQUEST
            )
        return success_response(
            message=auth_user["message"],
            data={"user": auth_user["user"], "token": auth_user["token"]},
            status_code=HTTPStatus.OK,
        )

    async def change_password(
        self, id: str, user_data: ChangeUserPasswordRequest
    ) -> tuple:
        updated_password = await self.auth_service.change_password(id, user_data)
        if not updated_password["is_success"]:
            return error_response(
                message=updated_password["message"], status_code=HTTPStatus.BAD_REQUEST
            )
        return success_response(
            message=updated_password["message"],
            status_code=HTTPStatus.OK,
        )
