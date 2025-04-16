from typing import TypedDict

from src import __name__, __version__, __description__, __display_name__
from src.utils.env import get_env_int, get_env_str, get_env_list


class Env:
    @property
    def isLocal(self) -> bool:
        return get_env_str("ENVIRONMENT") == "local"

    @property
    def isTest(self) -> bool:
        return get_env_str("ENVIRONMENT") == "test"

    @property
    def isProd(self) -> bool:
        return get_env_str("ENVIRONMENT") == "prod"


class App(TypedDict):
    name: str
    display_name: str
    version: str
    description: str
    secret_key: str
    debug: bool
    allowed_hosts: list[str]


class Log(TypedDict):
    level: str


class DB(TypedDict):
    mongo: dict[str, str | int]
    pg: dict[str, str | int]


class Cache(TypedDict):
    redis: dict[str, str | int]


class JWT(TypedDict):
    secret: str
    issuer: str


class OTP(TypedDict):
    lifetime: int


class RabbitMQ(TypedDict):
    host: str


env = Env()

app: App = {
    "name": __name__,
    "display_name": __display_name__,
    "version": __version__,
    "description": __description__,
    "secret_key": get_env_str("SECRET_KEY"),
    "debug": True if (env.isLocal or env.isTest) else False,
    "allowed_hosts": get_env_list("ALLOWED_HOSTS", default="*"),
}

log: Log = {
    "level": get_env_str("LOG_LEVEL", default="debug").upper(),
}

db: DB = {
    "mongo": {
        "host": get_env_str("MONGODB_HOST"),
        "port": get_env_int("MONGODB_PORT"),
        "user": get_env_str("MONGODB_USERNAME"),
        "pass": get_env_str("MONGODB_PASSWORD"),
        "database": get_env_str("MONGODB_DATABASE"),
    },
    "pg": {
        "host": get_env_str("PG_HOST"),
        "port": get_env_int("PG_PORT"),
        "user": get_env_str("PG_USERNAME"),
        "pass": get_env_str("PG_PASSWORD"),
        "database": get_env_str("PG_DATABASE"),
    },
}

cache: Cache = {
    "redis": {
        "host": get_env_str("REDIS_HOST"),
        "port": get_env_int("REDIS_PORT"),
        "user": get_env_str("REDIS_USERNAME"),
        "pass": get_env_str("REDIS_PASSWORD"),
    }
}


jwt_config: JWT = {
    "secret": get_env_str("JWT_SECRET"),
    "issuer": get_env_str("JWT_ISSUER"),
}

otp: OTP = {"lifetime": get_env_int("OTP_LIFETIME")}

rabbitmq_config: RabbitMQ = {"host": get_env_str("RABBITMQ_HOST")}

__all__ = ["app", "cache", "db", "env", "jwt_config", "log", "otp"]
