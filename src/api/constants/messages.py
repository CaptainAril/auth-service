from typing import TypedDict
from collections.abc import Callable


class RegistrationMessages(TypedDict):
    EMAIL_EXISTS: str
    USER_REGISTERED: str
    VERIFICATION_SUCCESS: str
    VERIFICATION_FAILED: str


class AuthMessages(TypedDict):
    UNAUTHORIZED: str
    INVALID_CRED: str
    NOT_VALIDATED: str
    NOT_ACTIVE: str
    NOT_ENABLED: str
    IS_DELETED: str
    SUCCESS: str
    TOKEN_ERROR: str
    TOKEN_SUCCESS: str


class OtpMessages(TypedDict):
    SEND_SUCCESS: str
    VALIDATE_SUCCESS: str
    VALIDATE_FAIL: str
    USER_VALIDATED: str


class UserMessages(TypedDict):
    DOESNT_EXIST: str
    SANITIZED: str
    INCORRECT_PASSWORD: str
    PASSWORD_CHANGED: str


class CommonMessages(TypedDict):
    INTERNAL_SERVER_ERROR: str
    JWT_GENERATED: str
    VALIDATION_ERROR: str


class PasswordResetMessages(TypedDict):
    EMAIL_SENT: str
    INVALID_TOKEN: str
    TOKEN_EXPIRED: str
    PASSWORD_RESET: str
    DOESNT_EXIST: str
    INACTIVE: str
    DISABLED: str


class Messages(TypedDict):
    REGISTRATION: RegistrationMessages
    AUTH: AuthMessages
    OTP: OtpMessages
    USER: UserMessages
    COMMON: CommonMessages
    PASSWORD_RESET: PasswordResetMessages


class DynamicCommonMessages(TypedDict):
    FETCHED_SUCCESS: Callable[[str], str]
    FETCHED_FAILED: Callable[[str], str]
    DELETED: Callable[[str], str]
    NOT_FOUND: Callable[[str], str]


class DynamicAccountMessages(TypedDict):
    EXISTS: Callable[[str], str]


class DynamicPasswordResetMessages(TypedDict):
    EMAIL_SENT: Callable[[str], str]


class DynamicMessages(TypedDict):
    COMMON: DynamicCommonMessages
    ACCOUNT: DynamicAccountMessages
    PASSWORD_RESET: DynamicPasswordResetMessages


MESSAGES: Messages = {
    "REGISTRATION": {
        "EMAIL_EXISTS": "Email already registered",
        "USER_REGISTERED": "User registration successful",
        "VERIFICATION_SUCCESS": "User email verification successful",
        "VERIFICATION_FAILED": "User email verification failed",
    },
    "AUTH": {
        "UNAUTHORIZED": "Unauthorized access",
        "INVALID_CRED": "Invalid email or password",
        "NOT_VALIDATED": "User account not validated. Please check your email for further instructions",
        "NOT_ACTIVE": "User account is inactive. Please contact support",
        "NOT_ENABLED": "User account is disabled. Please contact support",
        "IS_DELETED": "User account has been deleted. Please contact support if you want to restore your account",
        "SUCCESS": "Successfully logged in",
        "TOKEN_ERROR": "Invalid token",
        "TOKEN_SUCCESS": "Valid token",
    },
    "OTP": {
        "SEND_SUCCESS": "OTP sent successfully",
        "USER_VALIDATED": "User is already validated",
        "VALIDATE_SUCCESS": "OTP validation was successful",
        "VALIDATE_FAIL": "OTP validation failed",
    },
    "USER": {
        "DOESNT_EXIST": "User doesn't exist",
        "SANITIZED": "User object was sanitized",
        "INCORRECT_PASSWORD": "Incorrect old password",
        "PASSWORD_CHANGED": "Password changed successfully",
    },
    "COMMON": {
        "INTERNAL_SERVER_ERROR": "Something went wrong",
        "JWT_GENERATED": "JWT was generated",
        "VALIDATION_ERROR": "Validation errors",
    },
    "PASSWORD_RESET": {
        "EMAIL_SENT": "Password reset email sent successfully to your email",
        "PASSWORD_RESET": "Password reset successfully",
        "INVALID_TOKEN": "Invalid password reset token!",
        "DOESNT_EXIST": "You don't have an account with us yet!",
        "TOKEN_EXPIRED": "Password reset token has expired!",
        "INACTIVE": "You can only reset the password of an active account!",
        "DISABLED": "You can only reset the password of an enabled account!",
    },
}

DYNAMIC_MESSAGES: DynamicMessages = {
    "COMMON": {
        "FETCHED_SUCCESS": lambda x: f"{x} fetched successfully",
        "FETCHED_FAILED": lambda x: f"{x} fetch failed",
        "DELETED": lambda x: f"{x} successfully deleted",
        "NOT_FOUND": lambda x: f"{x} not found!",
    },
    "ACCOUNT": {
        "EXISTS": lambda x: f"You already have an account with the account number {x}!"
    },
    "PASSWORD_RESET": {
        "EMAIL_SENT": lambda x: f"Password reset email has been sent to {x}",
    },
}

__all__ = ["DYNAMIC_MESSAGES", "MESSAGES"]
