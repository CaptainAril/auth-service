from typing import TypedDict


class SignatureSources(TypedDict):
    gateway: str
    queue: str


SIGNATURE_SOURCES: SignatureSources = {
    "gateway": "Gateway",
    "queue": "Broker Queue",
}
