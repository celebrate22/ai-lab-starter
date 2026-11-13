"""Check whether this computer has the basics needed for the AI lab."""

from dataclasses import dataclass
import importlib
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


def check_nvidia_gpu() -> CheckResult:
    """Look for an NVIDIA GPU using NVIDIA's optional nvidia-smi command."""
    if not shutil.which("nvidia-smi"):
        return CheckResult("info", "NVIDIA GPU status unavailable (nvidia-smi not found)")

    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return CheckResult("info", "NVIDIA GPU status unavailable (nvidia-smi could not query it)")

    gpu_names = result.stdout.strip()
    if gpu_names:
        return CheckResult("ok", f"NVIDIA GPU detected: {gpu_names.splitlines()[0]}")
    return CheckResult("info", "nvidia-smi ran, but it reported no NVIDIA GPU")


def run_checks() -> list[CheckResult]:
    """Run the readiness checks and return their results."""
    return [
        check_python(),
        check_virtual_environment(),
        check_git(),
        check_package("numpy"),
        check_package("dotenv"),
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
