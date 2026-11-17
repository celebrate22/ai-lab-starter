import logging

import pytest

from ailab.logging_setup import setup_logging


@pytest.fixture(autouse=True)
def restore_logging():
    root = logging.getLogger()
    old_handlers = root.handlers[:]
    old_level = root.level
    yield
    for handler in root.handlers:
        if handler not in old_handlers:
            handler.close()
    root.handlers[:] = old_handlers
    root.setLevel(old_level)


def test_level_is_applied():
    setup_logging("debug")
    assert logging.getLogger().level == logging.DEBUG


def test_no_file_handler_by_default():
    setup_logging("INFO")
    handlers = logging.getLogger().handlers
    assert not any(isinstance(handler, logging.FileHandler) for handler in handlers)


def test_file_handler_writes_to_file(tmp_path):
    log_file = tmp_path / "run.log"
    setup_logging("INFO", str(log_file))
    logging.info("hello")
    for handler in logging.getLogger().handlers:
        handler.flush()
    assert "hello" in log_file.read_text(encoding="utf-8")


def test_calling_twice_does_not_duplicate_handlers():
    setup_logging("INFO")
    setup_logging("INFO")
    assert len(logging.getLogger().handlers) == 1
