import logging

import pytest

from ailab.logging_setup import setup_logging


@pytest.fixture(autouse=True)
def restore_logging():
    root = logging.getLogger()
    old_handlers = root.handlers[:]
    old_level = root.level
    yield                                   # the test runs here
    for h in root.handlers:
        if h not in old_handlers:
            h.close()
    root.handlers[:] = old_handlers
    root.setLevel(old_level)

def test_level_is_applied():
    setup_logging("debug")
    assert ...                      # the root logger's level equals logging.DEBUG


def test_no_file_handler_by_default():
    setup_logging("INFO")
    handlers = logging.getLogger().handlers
    assert ...                      # none of them is a logging.FileHandler


def test_file_handler_writes_to_file(tmp_path):
    log_file = tmp_path / "run.log"
    setup_logging("INFO", str(log_file))
    logging.info("hello")
    assert ...                      # "hello" appears in log_file.read_text()


def test_calling_twice_does_not_duplicate_handlers():
    setup_logging("INFO")
    setup_logging("INFO")
    assert ...                      # the root logger has exactly 1 handler