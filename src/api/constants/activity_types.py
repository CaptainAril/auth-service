from typing import TypedDict


class ActivityTypes(TypedDict):
    EXCEPTION: str
    USER_REGISTRATION: str
    SEND_OTP: str
    VALIDATE_OTP: str
    RESEND_EMAIL: str
    EMAIL_VALIDATION: str
    USER_LOGIN: str
    CHANGE_PASSWORD: str
    REQUEST_RESET_PASSWORD: str
    CONFIRM_RESET_PASSWORD: str


ACTIVITY_TYPES: ActivityTypes = {
    "EXCEPTION": "Exception handler",
    "USER_REGISTRATION": "User registration",
    "SEND_OTP": "Send OTP",
    "VALIDATE_OTP": "Validate OTP",
    "RESEND_EMAIL": "Resend email validation",
    "EMAIL_VALIDATION": "Email validation",
    "USER_LOGIN": "User login",
    "CHANGE_PASSWORD": "Change user password",
    "REQUEST_RESET_PASSWORD": "Request for password reset",
    "CONFIRM_RESET_PASSWORD": "Confirm password reset",
}

__all__ = ["ACTIVITY_TYPES"]
