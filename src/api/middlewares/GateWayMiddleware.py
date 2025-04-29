from django.http import HttpRequest
from ninja.errors import AuthenticationError
from ninja.security import APIKeyHeader
from ninja.openapi.schema import OpenAPISchema

from src.env import api_gateway
from src.utils.logger import Logger
from src.api.services.UtilityService import SignatureData, UtilityService
from src.api.constants.signature_sources import SIGNATURE_SOURCES


class GateWayAuth(APIKeyHeader):
    def __init__(self, logger: Logger) -> None:
        self.logger = logger
        super().__init__()

    def authenticate(self, request: HttpRequest, key: str | None) -> str | None:
        try:
            api_timestamp = request.headers["X-API-GATEWAY-TIMESTAMP"]
            api_signature = request.headers["X-API-GATEWAY-SIGNATURE"]
        except KeyError as e:
            message = f"Missing required header: {e}"
            self.logger.error(
                {
                    "activity_type": "Authenticate Gateway Request",
                    "message": message,
                    "metadata": {"headers": request.headers},
                }
            )
            raise AuthenticationError(message=message)

        signature_data: SignatureData = {
            "signature": api_signature,
            "timestamp": api_timestamp,
            "key": api_gateway["key"],
            "ttl": api_gateway["ttl"],
            "title": SIGNATURE_SOURCES["gateway"],
        }

        UtilityService.verify_signature(
            logger=self.logger, signature_data=signature_data
        )

        self.logger.debug(
            {
                "activity_type": "Authenticate Gateway Request",
                "message": "Successfully authenticated gateway request",
                "metadata": {
                    "headers": request.headers,
                },
            }
        )

        return api_signature


def get_authentication() -> GateWayAuth:
    gateway_auth = GateWayAuth(Logger("Authentication"))
    return gateway_auth


def add_global_headers(schema: OpenAPISchema) -> OpenAPISchema:
    for path in schema["paths"]:
        for method in schema["paths"][path]:
            operation = schema["paths"][path][method]
            if operation.get("security"):
                operation["security"] = schema["security"]
    return schema


authentication = get_authentication()
