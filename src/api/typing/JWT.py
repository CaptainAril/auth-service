from typing import TypedDict, NotRequired


class JWTData(TypedDict):
    email: str
    user_id: str


class JWTSuccess(TypedDict):
    is_success: bool
    message: str
    data: NotRequired[JWTData]
