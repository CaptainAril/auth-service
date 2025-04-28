from pathlib import Path
from functools import cache

from decouple import Config, AutoConfig, RepositoryEnv
from decouple import config as decouple_config

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"


@cache
def get_environment() -> Config | AutoConfig:
    if ENV_FILE.exists():
        return Config(RepositoryEnv(ENV_FILE))
    return decouple_config


get_env_variable = get_environment()


def get_env_str(name: str, default: str | None = None) -> str:
    return str(get_env_variable(name, default=default))


def get_env_int(name: str, default: str | None = None) -> int:
    return int(get_env_variable(name, default=default, cast=int))


def get_env_float(name: str, default: str | None = None) -> float:
    return float(get_env_variable(name, default=default, cast=float))


def get_env_list(name: str, sep: str = ",", default: str | None = None) -> list[str]:
    return list(
        get_env_variable(
            name, default=default, cast=lambda x: [v for v in x.split(sep)]
        )  # type: ignore
    )
