import traceback
from http import HTTPStatus

from django.http import HttpRequest, HttpResponse
from ninja.errors import ValidationError, AuthenticationError

from src.api.routes import api
from src.utils.logger import Logger
from src.api.constants.messages import MESSAGES
from src.api.constants.activity_types import ACTIVITY_TYPES

from .response_format import error_response

exception_logger = Logger("API Exception")


@api.exception_handler(AuthenticationError)
def on_invalid_token(request: HttpRequest, exc: Exception) -> HttpResponse:
    exception_logger.debug(
        {
            "activity_type": ACTIVITY_TYPES["EXCEPTION"],
            "message": MESSAGES["AUTH"]["UNAUTHORIZED"],
            "metadata": {"exception": exc.__class__},
        }
    )
    return api.create_response(
        request,
        error_response(
            message=MESSAGES["AUTH"]["UNAUTHORIZED"],
            status_code=HTTPStatus.UNAUTHORIZED,
        )[1],
        status=HTTPStatus.UNAUTHORIZED,
    )


@api.exception_handler(ValidationError)
def on_validation_error(request: HttpRequest, exc: ValidationError) -> HttpResponse:
    exception_logger.error(
        {
            "activity_type": ACTIVITY_TYPES["EXCEPTION"],
            "message": str(exc),
            "metadata": {"exception": exc.__class__},
        }
    )
    errors = exc.errors
    return api.create_response(
        request,
        error_response(
            message=MESSAGES["COMMON"]["VALIDATION_ERROR"],
            errors=errors,
            status_code=HTTPStatus.BAD_REQUEST,
        )[1],
        status=HTTPStatus.BAD_REQUEST,
    )


@api.exception_handler(Exception)
def on_server_error(request: HttpRequest, exc: Exception) -> HttpResponse:
    exception_logger.error(
        {
            "activity_type": ACTIVITY_TYPES["EXCEPTION"],
            "message": str(
                [
                    {
                        "filename": x.filename,
                        "function": x.name,
                        "lineno": x.lineno,
                        "line": x.line,
                    }
                    for x in traceback.extract_tb(exc.__traceback__)
                ]
            )
            + f"\nmessage: {exc}",
            "metadata": {"exception": exc.__class__},
        }
    )
    return api.create_response(
        request,
        error_response(
            message=MESSAGES["COMMON"]["INTERNAL_SERVER_ERROR"],
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        )[1],
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )
