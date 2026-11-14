"""Time NumPy matrix multiplication and save the results as JSON."""

import argparse
import json
from pathlib import Path
import platform
import time

import numpy as np


def run_benchmark(
    matrix_size: int = 512,
    repetitions: int = 5,
    seed: int = 42,
) -> dict[str, object]:
    """Run repeated square-matrix multiplications and return measurements."""
    if matrix_size <= 0:
        raise ValueError("matrix_size must be greater than zero")
    if repetitions <= 0:
        raise ValueError("repetitions must be greater than zero")
    if seed < 0:
        raise ValueError("seed cannot be negative")

    random = np.random.default_rng(seed)
    left = random.random((matrix_size, matrix_size), dtype=np.float32)
    right = random.random((matrix_size, matrix_size), dtype=np.float32)

    # Run once before timing so first-use setup does not skew the measurements.
    left @ right

    durations = []
    for _ in range(repetitions):
        start = time.perf_counter()
        product = left @ right
        durations.append(time.perf_counter() - start)

    # Keep a reference to the final result until after timing is complete.
    del product

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
