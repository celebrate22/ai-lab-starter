"""Time NumPy matrix multiplication and save the results as JSON."""

import argparse
import json
from pathlib import Path
import platform
import time

import numpy as np

MAX_MATRIX_SIZE = 4096


def run_benchmark(
    matrix_size: int = 512,
    repetitions: int = 5,
    seed: int = 42,
) -> dict[str, object]:
    """Run repeated square-matrix multiplications and return measurements.

    The size limit keeps accidental command-line inputs from allocating
    unexpectedly large arrays. Three float32 matrices at the maximum size
    occupy about 192 MiB, before any temporary memory used by NumPy's backend.
    """
    if isinstance(matrix_size, bool) or not isinstance(matrix_size, int):
        raise ValueError("matrix_size must be a whole number")
    if matrix_size <= 0:
        raise ValueError("matrix_size must be greater than zero")
    if matrix_size > MAX_MATRIX_SIZE:
        raise ValueError(f"matrix_size cannot be greater than {MAX_MATRIX_SIZE}")
    if isinstance(repetitions, bool) or not isinstance(repetitions, int):
        raise ValueError("repetitions must be a whole number")
    if repetitions <= 0:
        raise ValueError("repetitions must be greater than zero")
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise ValueError("seed must be a whole number")
    if seed < 0:
        raise ValueError("seed cannot be negative")

    # Make repeatable input matrices from the requested seed.
    random = np.random.default_rng(seed)
    left = random.random((matrix_size, matrix_size), dtype=np.float32)
    right = random.random((matrix_size, matrix_size), dtype=np.float32)

    # Run once before timing so first-use setup does not skew the measurements.
    warm_up_result = left @ right
    del warm_up_result

    # Time only the multiplication. Delete each output after stopping the timer.
    durations = []
    for _ in range(repetitions):
        start = time.perf_counter()
        product = left @ right
        duration = time.perf_counter() - start
        del product
        durations.append(duration)

    return {
        "matrix_size": matrix_size,
        "repetitions": repetitions,
        "seed": seed,
        "dtype": "float32",
        "python_version": platform.python_version(),
        "numpy_version": np.__version__,
        "platform": platform.platform(),
        "durations_seconds": durations,
        "average_seconds": sum(durations) / len(durations),
        "fastest_seconds": min(durations),
    }


def main() -> int:
    """Run the benchmark and save it to the selected JSON file."""
    # Read command-line options, run the calculation, then save its record.
    parser = argparse.ArgumentParser(
        description="Measure NumPy matrix multiplication on this machine."
    )
    parser.add_argument(
        "--environment",
        choices=("local", "colab"),
        default="local",
        help="label describing where this run is performed",
    )
    parser.add_argument("--size", type=int, default=512, help="rows and columns per matrix")
    parser.add_argument("--repetitions", type=int, default=5, help="number of timed runs")
    parser.add_argument("--seed", type=int, default=42, help="random input seed")
    parser.add_argument(
        "--output",
        type=Path,
        help="where to save JSON (default: results/<environment>_benchmark.json)",
    )
    args = parser.parse_args()

    try:
        results = run_benchmark(args.size, args.repetitions, args.seed)
    except ValueError as error:
        parser.error(str(error))

    results["environment"] = args.environment
    output_path = args.output or Path("results") / f"{args.environment}_benchmark.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")

    print(f"Average matrix multiplication time: {results['average_seconds']:.4f} seconds")
    print(f"Fastest run: {results['fastest_seconds']:.4f} seconds")
    print(f"Results saved to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
