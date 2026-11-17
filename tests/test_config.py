from dataclasses import FrozenInstanceError

import pytest

from ailab import config
from ailab.config import get_key, load_settings


def test_get_key_missing(monkeypatch):
    monkeypatch.delenv("TEST_KEY", raising=False)
    with pytest.raises(RuntimeError):
        get_key("TEST_KEY")


def test_get_key_present(monkeypatch):
    monkeypatch.setenv("TEST_KEY", "abc")
    assert get_key("TEST_KEY") == "abc"

def test_load_settings_defaults(monkeypatch):
    monkeypatch.setattr(config, "load_dotenv", lambda: None)
    monkeypatch.delenv("LOG_LEVEL", raising=False)
    monkeypatch.delenv("DATA_DIR", raising=False)
    settings = load_settings()
    assert settings.log_level == "INFO"
    assert settings.data_dir == "data"


def test_load_settings_reads_environment_variables(monkeypatch):
    monkeypatch.setattr(config, "load_dotenv", lambda: None)
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("DATA_DIR", "sample-data")
    settings = load_settings()
    assert settings.log_level == "DEBUG"
    assert settings.data_dir == "sample-data"


def test_settings_values_cannot_be_reassigned():
    settings = config.Settings(log_level="INFO", data_dir="data")
    with pytest.raises(FrozenInstanceError):
        settings.log_level = "DEBUG"
