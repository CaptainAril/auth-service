from http import HTTPStatus

from ninja import Router
from django.http import HttpRequest

from src.utils.svcs import ADepends
from src.api.controllers.AuthController import AuthController
from src.api.models.payload.responses.User import UserResponse, UserLoginResponse
from src.api.models.payload.requests.ResendUserOtp import ResendUserOtp
from src.api.models.payload.responses.ErrorResponse import (
    ErrorResponse,
    ServerErrorResponse,
)
from src.api.models.payload.responses.SuccessResponse import SuccessResponse
from src.api.models.payload.requests.CreateUserRequest import CreateUserRequest
from src.api.models.payload.requests.AuthenticateUserOtp import AuthenticateUserOtp
from src.api.models.payload.requests.AuthenticateUserRequest import (
    AuthenticateUserRequest,
)
from src.api.models.payload.requests.ChangeUserPasswordRequest import (
    ChangeUserPasswordRequest,
)

router = Router()


@router.post(
    "/register",
    response={
        HTTPStatus.CREATED: SuccessResponse[UserResponse],
        HTTPStatus.BAD_REQUEST: ErrorResponse,
        HTTPStatus.INTERNAL_SERVER_ERROR: ServerErrorResponse,
    },
)
async def create_user(request: HttpRequest, user_data: CreateUserRequest) -> tuple:
    auth_controller = await ADepends(AuthController)
    return await auth_controller.register(user_data)


@router.put(
    "/email/resend",
    response={
        HTTPStatus.OK: SuccessResponse,
        HTTPStatus.BAD_REQUEST: ErrorResponse,
        HTTPStatus.INTERNAL_SERVER_ERROR: ServerErrorResponse,
    },
)
async def resend_email(request: HttpRequest, credentials: ResendUserOtp) -> tuple:
    auth_controller = await ADepends(AuthController)
    return await auth_controller.resend_email(credentials)


@router.put(
    "/email/verification",
    response={
        HTTPStatus.OK: SuccessResponse,
        HTTPStatus.BAD_REQUEST: ErrorResponse,
        HTTPStatus.INTERNAL_SERVER_ERROR: ServerErrorResponse,
    },
)
async def validate_email(
    request: HttpRequest, credentials: AuthenticateUserOtp
) -> tuple:
    auth_controller = await ADepends(AuthController)
    return await auth_controller.validate_email(credentials)


@router.post(
    "/login",
    response={
        HTTPStatus.OK: SuccessResponse[UserLoginResponse],
        HTTPStatus.BAD_REQUEST: ErrorResponse,
        HTTPStatus.INTERNAL_SERVER_ERROR: ServerErrorResponse,
    },
)
async def login(request: HttpRequest, credentials: AuthenticateUserRequest) -> tuple:
    auth_controller = await ADepends(AuthController)
    return await auth_controller.login(credentials)


@router.put(
    "/change-password",
    response={
        HTTPStatus.OK: SuccessResponse,
        HTTPStatus.BAD_REQUEST: ErrorResponse,
        HTTPStatus.INTERNAL_SERVER_ERROR: ServerErrorResponse,
    },
)
async def update_password(
    request: HttpRequest, user_data: ChangeUserPasswordRequest
) -> tuple:
    user_id = getattr(request, "auth_id", "")
    auth_controller = await ADepends(AuthController)
    return await auth_controller.change_password(user_id, user_data)
