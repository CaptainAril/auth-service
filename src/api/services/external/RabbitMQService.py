import atexit
import threading
from typing import Annotated
from functools import partial
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor

import pika
from pika import spec
from pika.channel import Channel
from pika.adapters.blocking_connection import BlockingChannel

from src.env import rabbitmq_config
from src.utils.svcs import Service
from src.utils.logger import Logger


@Service()
class RabbitMQService:
    def __init__(self, logger: Annotated[Logger, "RabbitMQService"]) -> None:
        self.logger = logger
        self.__params = pika.ConnectionParameters(rabbitmq_config["host"])
        self.__connection = None
        self.__callbacks: dict[str, Callable] = {}

        self.__executor = ThreadPoolExecutor()

        with threading.RLock():
            atexit.register(self.close)

    def __connect(self, fn: str) -> tuple[pika.BlockingConnection, BlockingChannel]:
        if self.__connection is None or self.__connection.is_closed:
            self.__connection = pika.BlockingConnection(self.__params)
            self.logger.info(f"Connected to RabbitMQ, from {fn}")
        return self.__connection, self.__connection.channel()

    def __publish_message(self, queue_name: str, message: str) -> None:
        connection, channel = self.__connect("publish")

        channel.queue_declare(queue=queue_name, durable=True)
        channel.basic_publish(
            exchange="",
            routing_key=queue_name,
            body=message.encode(),
            properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent),
        )
        self.logger.debug(f"Published message to queue {queue_name}")
        channel.close()
        connection.close()

    def publish(self, queue_name: str, message: str) -> None:
        self.__executor.submit(self.__publish_message, queue_name, message)

    def __process_message(
        self,
        ch: Channel,
        method: spec.Basic.Deliver,
        properties: spec.BasicProperties,
        body: bytes,
        queue_name: str,
    ) -> None:
        try:
            self.__callbacks[queue_name](body.decode())
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
        finally:
            ch.basic_ack(delivery_tag=method.delivery_tag)

    def __consume(self, queue_name: str) -> None:
        connection, channel = self.__connect("consume")

        channel.queue_declare(queue=queue_name, durable=True)
        channel.basic_qos(prefetch_count=1)

        channel.basic_consume(
            queue=queue_name,
            on_message_callback=partial(self.__process_message, queue_name=queue_name),
            exclusive=True,
        )
        channel.start_consuming()
        channel.close()
        connection.close()

    def register_callback(
        self, queue_name: str, callback: Callable[[str], None]
    ) -> None:
        if queue_name in self.__callbacks:
            if self.__callbacks[queue_name] != callback:
                self.__callbacks[queue_name] = callback
            return

        self.__callbacks[queue_name] = callback
        self.__executor.submit(self.__consume, queue_name)

    def close(self) -> None:
        self.__executor.shutdown(wait=False)
