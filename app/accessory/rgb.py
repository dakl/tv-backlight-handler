from typing import Tuple

import structlog
from requests import post

from app import config

from .base import Accessory

logger = structlog.getLogger(__name__)

STATE_MAP = {
    'ON': 1,
    'OFF': 0,
}


class RGBLight(Accessory):
    def __init__(self,
                 name,
                 device_id=None,
                 access_token=None,
                 base_url=None,
                 headers=None,
                 payload_factory=None):
        self.name = name
        self.device_id = device_id or config.TV_BACKLIGHT_DEVICE_ID
        self.access_token = access_token or config.PARTICLE_ACCESS_TOKEN
        self.base_url = base_url or config.PARTICLE_BASE_URL
        self.headers = headers or {
            "Content-type": "application/x-www-form-urlencoded"
        }

    def _get_payload(self, access_token, value=None):
        payload = {'access_token': access_token}
        if value is not None:
            payload['args'] = value
        return payload

    def _set_parameter(self, parameter, value):
        payload = self._get_payload(self.access_token, value=value)
        url = self._get_url(parameter)
        logger.info("Sending args", args=payload.get('args'))
        response = post(url, data=payload, headers=self.headers)
        return response.json().get('return_value')

    def set_status(self, value):
        """1 means on, 0 means off"""
        return self._set_parameter('state', value)

    def set_brightness(self, value: int) -> None:
        """ Brightness is expected to come in as an int in the range 0-100."""
        return self._set_parameter('brightness', value)

    def set_color(self, r: int, g: int, b: int):
        return self._set_parameter('color', f'{r},{g},{b}')

    def get_status(self):
        return 0

    def get_brightness(self) -> int:
        # payload = self._get_payload(self.access_token)
        # url = self._get_url('brightness')
        # response = get(url, payload, headers=self.headers)
        return 0

    def get_color(self) -> Tuple[int, int, int]:
        return (0, 0, 0)

    def handle(self, payload):
        if 'brightness' in payload:
            b = int(100 * payload.get('brightness') / 255)
            self.set_brightness(b)
        if 'color' in payload:
            color = payload.get('color')
            self.set_color(**color)
        if 'state' in payload:
            if payload.get('state') == 'OFF':
                self.set_status(STATE_MAP[payload.get('state')])

        if list(payload.keys()) == ['state'] and payload.get('state') == 'ON':
            # if the only param is state, make it yellow-ish
            self.set_brightness(70)
