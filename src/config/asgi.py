"""
ASGI config for src project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from faststream.rabbit import RabbitBroker
from starlette.routing import Mount
from starlette.applications import Starlette

from src.env import rabbitmq_config

broker = RabbitBroker(host=rabbitmq_config["host"])


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.config.settings")

django_application = get_asgi_application()

application = Starlette(
    routes=[Mount("/", get_asgi_application())],
    on_startup=[broker.start],
    on_shutdown=[broker.close],
)


from src.api.services.external import RabbitMQRoutes as RabbitMQRoutes  # noqa: E402
