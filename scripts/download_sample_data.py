"""Download a small public sample file into the project's data folder."""

import argparse
import math
import os
from pathlib import Path
import re
import tempfile
from urllib.parse import unquote, urlparse
from urllib.request import urlopen


DEFAULT_MAX_BYTES = 10 * 1024 * 1024
CHUNK_SIZE = 64 * 1024


def download_sample(
    url: str,
    filename: str | None = None,
    max_bytes: int = DEFAULT_MAX_BYTES,
    data_dir: Path = Path("data"),
    force: bool = False,
) -> Path:
    """Download an HTTPS URL without exceeding the byte limit.

    The response is streamed to a temporary file and moved into place only
    after the full download succeeds, so an interrupted download is not left
    looking like a complete sample.
    """
    parsed_url = urlparse(url)
    if parsed_url.scheme != "https" or not parsed_url.hostname:
        raise ValueError("url must be a valid HTTPS address")
    if isinstance(max_bytes, bool) or not isinstance(max_bytes, int) or max_bytes <= 0:
        raise ValueError("max_bytes must be a positive whole number")

    if filename is None:
        filename = unquote(Path(parsed_url.path).name)
    if (
        not filename
        or filename in {".", ".."}
        or Path(filename).name != filename
        or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", filename)
    ):
        raise ValueError("filename must be a simple name containing letters, numbers, dots, _ or -")

    destination = data_dir / filename
    if destination.exists() and not force:
        raise FileExistsError(f"{destination} already exists; use --force to replace it")

    data_dir.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with urlopen(url, timeout=20) as response:
            final_url = urlparse(response.geturl())
            if final_url.scheme != "https":
                raise ValueError("download redirected to a non-HTTPS address")

            with tempfile.NamedTemporaryFile(
                mode="wb", dir=data_dir, prefix=f".{filename}.", suffix=".part", delete=False
            ) as temporary_file:
                temporary_path = Path(temporary_file.name)
                total_bytes = 0
                while chunk := response.read(CHUNK_SIZE):
                    total_bytes += len(chunk)
                    if total_bytes > max_bytes:
                        raise ValueError(f"download exceeds the {max_bytes}-byte limit")
                    temporary_file.write(chunk)

        if destination.exists() and not force:
            raise FileExistsError(f"{destination} already exists; use --force to replace it")
        os.replace(temporary_path, destination)
        return destination
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="HTTPS URL of a public sample file")
    parser.add_argument("--filename", help="safe output filename (default: name from URL)")
    parser.add_argument(
        "--max-mb", type=float, default=10,
        help="maximum download size in decimal megabytes (default: 10)",
    )
    parser.add_argument("--force", action="store_true", help="replace an existing file")
    args = parser.parse_args()
    if not math.isfinite(args.max_mb) or args.max_mb <= 0:
        parser.error("--max-mb must be a finite number greater than zero")

    try:
        output = download_sample(
            args.url,
            args.filename,
            int(args.max_mb * 1_000_000),
            force=args.force,
        )
    except (OSError, ValueError) as error:
        parser.error(str(error))

    print(f"Sample data saved to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
