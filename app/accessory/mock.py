from typing import Tuple
from .base import Accessory


class MockAccessory(Accessory):
    def set_status(self, value) -> int:
        return 1

    def set_brightness(self, value: int) -> int:
        return 1

    def set_color(self, r: int, g: int, b: int) -> int:
        return 1

    def get_status(self):
        return 0

    def get_brightness(self) -> float:
        return 0

    def get_color(self) -> Tuple[int, int, int]:
        return (0, 0, 0)
