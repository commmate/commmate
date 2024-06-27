import os

class Config:
    _instance = None
    _config_obj = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not self._config_obj:
            environment = os.getenv('APP_ENV', 'local').lower()
            self.config_map = {
                'testing': Testing(),
                'local': Local(),
                'development': Development(),
                'staging': Staging(),
                'production': Production()
            }
            self._config_obj = self.config_map.get(environment, Local())
            self._config_obj.APP_ENV = environment

    def __getattr__(self, name):
        if hasattr(self._config_obj, name):
            return getattr(self._config_obj, name)
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")


class Base:
    """Common configuration."""

    OPENAI_ORGANIZATION_ID = os.getenv('OPENAI_ORGANIZATION_ID')
    OPENAI_PROJECT_ID = os.getenv('OPENAI_PROJECT_ID')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    STORMGLASS_API_KEY = os.getenv('STORMGLASS_API_KEY')
    GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')


class Testing(Base):
    """Configuration used in unit tests."""
    DEBUG = True


class Local(Base):
    """Configuration used in LOCAL machines."""
    DEBUG = True


class Development(Base):
    """Configuration used in DEV servers."""
    DEBUG = False


class Staging(Base):
    """Configuration used in STAGING servers."""
    DEBUG = False


class Production(Base):
    """Configuration used in PROD servers."""
    DEBUG = False
