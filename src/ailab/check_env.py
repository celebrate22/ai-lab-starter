"""Check whether this computer has the basics needed for the AI lab."""

from dataclasses import dataclass
import csv
import importlib
import io
import shutil
import subprocess
import sys


@dataclass(frozen=True)
class CheckResult:
    """One check's label and the message to show the user."""

    status: str
    message: str


def check_python() -> CheckResult:
    """Require Python 3.10 or newer, as declared in pyproject.toml."""
    version = sys.version_info
    version_text = f"Python {version.major}.{version.minor}.{version.micro}"

    if version >= (3, 10):
        return CheckResult("ok", version_text)
    return CheckResult("error", f"{version_text}; Python 3.10 or newer is required")


def check_virtual_environment() -> CheckResult:
    """Recommend using an isolated Python environment for this project."""
    if sys.prefix != sys.base_prefix:
        return CheckResult("ok", "virtual environment is active")
    return CheckResult("warn", "no virtual environment detected")


def check_git() -> CheckResult:
    """Check whether the Git command is available on this computer."""
    if shutil.which("git"):
        return CheckResult("ok", "Git command is available")
    return CheckResult("warn", "Git command was not found")


def check_package(module_name: str) -> CheckResult:
    """Check whether a Python package can be imported."""
    try:
        importlib.import_module(module_name)
    except ImportError:
        return CheckResult("error", f"{module_name} is not importable")
    return CheckResult("ok", f"{module_name} is importable")


def _format_gib(bytes_value: int) -> str:
    """Turn a byte count into a readable number of GiB."""
    gib = bytes_value / (1024**3)
    return f"{gib:.1f} GiB"


def check_system_memory() -> CheckResult:
    """Report total, used, and currently available system RAM."""
    try:
        # Import here so this checker can still report a missing psutil package.
        psutil = importlib.import_module("psutil")
        memory = psutil.virtual_memory()
    except ImportError:
        return CheckResult("error", "system memory unavailable (psutil is not importable)")
    except OSError:
        return CheckResult("info", "system memory status unavailable")

    return CheckResult(
        "ok",
        "System RAM: "
        f"{_format_gib(memory.total)} total, "
        f"{_format_gib(memory.used)} used, "
        f"{_format_gib(memory.available)} available",
    )


def check_nvidia_gpu() -> CheckResult:
    """Report NVIDIA GPU names and memory using the optional nvidia-smi command."""
    if not shutil.which("nvidia-smi"):
        return CheckResult("info", "NVIDIA GPU status unavailable (nvidia-smi not found)")

    try:
        result = subprocess.run(
            [
                "nvidia-smi",
                "--query-gpu=index,name,memory.total,memory.used,memory.free",
                "--format=csv,noheader,nounits",
            ],
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return CheckResult("info", "NVIDIA GPU status unavailable (nvidia-smi could not query it)")

    # NVIDIA prints one comma-separated row per GPU. With nounits enabled,
    # the three memory values are integers in MiB; 1 GiB equals 1024 MiB.
    gpu_rows = list(csv.reader(io.StringIO(result.stdout), skipinitialspace=True))
    gpu_reports = []
    memory_reported = True
    for row in gpu_rows:
        if not row:
            continue

        # Older or restricted tools may return just a GPU name.
        if len(row) == 1 and row[0].strip():
            gpu_reports.append(
                f"NVIDIA GPU detected: {row[0].strip()}; memory details unavailable"
            )
            continue

        # Keep the GPU name useful even if a driver cannot report its memory.
        if len(row) < 2:
            continue
        gpu_index, gpu_name = row[0].strip(), row[1].strip()
        if len(row) >= 5:
            try:
                total_mib, used_mib, free_mib = (int(value.strip()) for value in row[2:5])
            except ValueError:
                memory_reported = False
            else:
                gpu_reports.append(
                    f"GPU {gpu_index} {gpu_name}: "
                    f"{total_mib / 1024:.1f} GiB total, "
                    f"{used_mib / 1024:.1f} GiB used, "
                    f"{free_mib / 1024:.1f} GiB free"
                )
                continue

        memory_reported = False
        gpu_reports.append(f"GPU {gpu_index} {gpu_name}: memory details unavailable")

    if not gpu_reports:
        return CheckResult("info", "nvidia-smi ran, but it reported no readable NVIDIA GPU")

    status = "ok" if memory_reported else "info"
    return CheckResult(status, "; ".join(gpu_reports))


def run_checks() -> list[CheckResult]:
    """Run the readiness checks and return their results."""
    return [
        check_python(),
        check_virtual_environment(),
        check_git(),
        check_package("numpy"),
        check_package("dotenv"),
        check_package("psutil"),
        check_system_memory(),
        check_nvidia_gpu(),
    ]


def main() -> int:
    """Print check results; return a failing exit code if a required check fails."""
    results = run_checks()
    for result in results:
        print(f"[{result.status}] {result.message}")

    return int(any(result.status == "error" for result in results))


if __name__ == "__main__":
    raise SystemExit(main())
