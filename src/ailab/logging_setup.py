import logging


def setup_logging(level: str = "INFO", log_file: str | None = None) -> None:
    """Send log messages to the terminal and, optionally, to a file."""
    # A handler is the destination where a log message is written.
    handlers: list[logging.Handler] = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_file))

    # Only show messages at this importance level or higher.
    logging.basicConfig(
        level=level.upper(),
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=handlers,
        # Replace existing logging setup, so calling this function twice is safe.
        force=True,
    )
