import os
from dotenv import load_dotenv, find_dotenv

env_file = find_dotenv()
load_dotenv(env_file)


class Settings:
    LOGGING_LEVEL = os.environ.get("LOGGING_LEVEL", "DEBUG")
    ALPHA_VANTAGE_API_KEY = os.environ.get("ALPHA_VANTAGE_API_KEY")

    @classmethod
    def show_keys(cls):
        attrs = [k for k in dir(cls) if k.isupper() and not k.startswith("_")]
        return {k: getattr(cls, k) for k in attrs}
