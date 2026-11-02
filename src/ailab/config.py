import os

def get_key(name: str) -> str:
    value = os.getenv(name)
    if value == None or value == "":
        raise RuntimeError(f"{name} is not set. Add it to your .env file.")
    return value