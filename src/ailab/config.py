import os
from dataclasses import dataclass
from dotenv import load_dotenv

@dataclass(frozen=True)
class Settings:
    log_level: str
    data_dir: str

def get_key(name: str) -> str:
    value = os.getenv(name)
    if value == None or value == "":
        raise RuntimeError(f"{name} is not set. Add it to your .env file.")
    return value


def load_settings() -> Settings:
    load_dotenv()
    return Settings(
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        data_dir=os.getenv("DATA_DIR", "data"),
    )

