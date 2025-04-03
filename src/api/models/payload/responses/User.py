from uuid import UUID

from ninja import Schema, ModelSchema

from src.api.models.postgres import User as UserModel


class UserResponse(ModelSchema):
    id: UUID

    class Meta:
        model = UserModel
        fields = (
            "id",
            "email",
        )


class UserLoginResponse(Schema):
    user: UserResponse
    token: str
