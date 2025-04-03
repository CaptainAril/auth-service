from ninja import NinjaAPI
from django.http import HttpRequest

from src.env import app

api: NinjaAPI = NinjaAPI(
    version=app["version"],
    title=app["display_name"],
    description=app["description"],
)

from src.api.utils import error_handlers  # noqa: E402, F401


@api.get("/")
async def home(request: HttpRequest) -> dict:
    return {"message": "Hello, World!"}


api.add_router("/auth", "src.api.routes.Auth.router", tags=["Auth"])
api.add_router(
    "/password/reset", "src.api.routes.PasswordReset.router", tags=["Password"]
)
