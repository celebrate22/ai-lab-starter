import pytest

from ailab.config import get_key, load_settings


def test_get_key_missing(monkeypatch):
    monkeypatch.delenv("TEST_KEY", raising=False)
    with pytest.raises(RuntimeError):
        get_key("TEST_KEY")


def test_get_key_present(monkeypatch):
    monkeypatch.setenv("TEST_KEY", "abc")
    assert get_key("TEST_KEY") == "abc"

def test_load_settings_defaults(monkeypatch):
    monkeypatch.delenv("LOG_LEVEL", raising=False)
    monkeypatch.delenv("DATA_DIR", raising=False)
    settings = load_settings()
    assert settings.log_level == "INFO"
    assert settings.data_dir == "data"