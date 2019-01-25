from typing import Dict

from app.accessory.base import Accessory
from app.accessory.rgb import RGBLight

ACCESSORIES: Dict[int, Accessory] = {
    1: RGBLight(name='tv-backlight'),
}
