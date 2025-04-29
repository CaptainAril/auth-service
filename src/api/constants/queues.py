from typing import TypedDict


class QueueNames(TypedDict):
    USER_REGISTRATION: str
    EMAIL_VALIDATION: str


QUEUE_NAMES: QueueNames = {
    "USER_REGISTRATION": "create_user",
    "EMAIL_VALIDATION": "validate_email",
}
