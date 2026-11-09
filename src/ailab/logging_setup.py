import logging


def setup_logging(level: str = "INFO", log_file: str | None = None) -> None:
    handlers: list[logging.Handler] = [logging.StreamHandler()]  # a StreamHandler, which writes to the terminal
    if log_file:
        handlers.append(logging.FileHandler(log_file))          # a FileHandler, which writes to that file
    logging.basicConfig(
        level=level.upper(),                                    # the level string in uppercase
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=handlers,
        force=True,
    )
