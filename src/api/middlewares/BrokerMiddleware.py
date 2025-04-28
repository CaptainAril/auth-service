from types import CoroutineType
from typing import Any
from collections.abc import Callable, Awaitable

from faststream import BaseMiddleware
from faststream.broker.message import StreamMessage
from faststream.rabbit.message import RabbitMessage

from src.env import queue
from src.utils.logger import Logger
from src.api.services.UtilityService import UtilityService
from src.api.constants.signature_sources import SIGNATURE_SOURCES


class PublishMiddleware(BaseMiddleware):
    """
    Middleware to handle subscription messages.
    """

    async def publish_scope(
        self,
        call_next: Callable[..., Awaitable[Any]],
        msg: RabbitMessage,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any],
    ) -> CoroutineType:
        timestamp = UtilityService.get_timestamp()
        signature = UtilityService.generate_signature(queue["key"], timestamp)

        headers = {}

        headers["X-BROKER-SIGNATURE"] = signature
        headers["X-BROKER-TIMESTAMP"] = timestamp
        headers["X-BROKER-KEY"] = queue["key"]

        kwargs["headers"] = headers
        return await super().publish_scope(call_next, msg, *args, **kwargs)


class SubscribeMiddleware(BaseMiddleware):
    async def consume_scope(
        self, call_next: Callable[[Any], Awaitable[Any]], msg: StreamMessage
    ) -> CoroutineType | None:
        logger = Logger(__name__)
        try:
            UtilityService.verify_signature(
                logger=logger,
                signature_data={
                    "signature": msg.headers["X-BROKER-SIGNATURE"],
                    "timestamp": msg.headers["X-BROKER-TIMESTAMP"],
                    "key": queue["key"],
                    "ttl": queue["ttl"],
                    "title": SIGNATURE_SOURCES["gateway"],
                },
            )

            return await super().consume_scope(call_next, msg)
        except KeyError as e:
            message = f"Missing required header: {e}"
            logger.error(
                {
                    "activity_type": "Authenticate GatewaBroker Queue Request",
                    "message": message,
                    "metadata": {"headers": msg.headers},
                }
            )
        except Exception as e:
            queue_operation = msg.raw_message.routing_key
            message = f"`{queue_operation}` operation failed: {e}"
            logger.error(
                {
                    "activity_type": "Authenticate GatewaBroker Queue Request",
                    "message": message,
                    "metadata": {"headers": msg.headers, "message": msg._decoded_body},
                }
            )
