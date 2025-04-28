"""
ASGI config for src project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from faststream.rabbit import RabbitBroker
from starlette.applications import Starlette
from starlette.routing import Mount

from src.env import rabbitmq_config

broker = RabbitBroker(rabbitmq_config["url"])


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.config.settings")


def setup_broker_middlewares():
    from src.api.middlewares.BrokerMiddleware import (PublishMiddleware,
                                                      SubscribeMiddleware)

    broker.add_middleware(SubscribeMiddleware)
    broker.add_middleware(PublishMiddleware)


application = Starlette(
    routes=[Mount("/", get_asgi_application())],  # type: ignore
    on_startup=[setup_broker_middlewares, broker.start],
    on_shutdown=[broker.close],
)


from src.api.services.external import \
    RabbitMQRoutes as RabbitMQRoutes  # noqa: E402
