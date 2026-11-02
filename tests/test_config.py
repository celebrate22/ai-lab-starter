import pytest

from ailab.config import get_key


def test_get_key_missing(monkeypatch):
    monkeypatch.delenv("TEST_KEY", raising=False)
    with pytest.raises(RuntimeError):
        get_key("TEST_KEY")


def test_get_key_present(monkeypatch):
    monkeypatch.setenv("TEST_KEY", "abc")
    assert get_key("TEST_KEY") == "abc"