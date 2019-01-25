from abc import ABC, abstractmethod


class Accessory(ABC):
    name: str

    def __init__(self, name):
        self.name = name

    def _get_url(self, endpoint):
        return f"{self.base_url}/{self.device_id}/{endpoint}"
