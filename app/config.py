import os
import logging

logger = logging.getLogger(__name__)


class Config:
    PARTICLE_BASE_URL = 'https://api.particle.io/v1/devices'
    BROKER = 'worker0'
    DEBUG = os.getenv('DEBUG', False)

    def __init__(self):
        self.TV_BACKLIGHT_DEVICE_ID = self.get_secret('TV_BACKLIGHT_DEVICE_ID')
        self.PARTICLE_ACCESS_TOKEN = self.get_secret('PARTICLE_ACCESS_TOKEN')

    def get_secret(self, secret_name):
        secret_file = f'/run/secrets/{secret_name.lower()}'
        if os.path.exists(secret_file):
            logger.info(f"Reading {secret_name} from docker secrets")
            with open(secret_file, 'r') as f:
                return f.readline().strip()
        else:
            logger.info(f"Reading {secret_name} from environment")
            return os.getenv(secret_name)
