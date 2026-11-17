"""Estimate the memory needed to store a model's parameters."""

import argparse


# Number of bits used to store one parameter in each supported format.
BITS_PER_PARAMETER = {
    "fp32": 32,
    "fp16": 16,
    "bf16": 16,
    "int8": 8,
    "int4": 4,
}


def estimate_memory_gb(parameter_count: int, precision: str) -> float:
    """Estimate parameter storage in decimal gigabytes (GB)."""
    # Reject bad inputs before doing the memory calculation.
    if isinstance(parameter_count, bool) or not isinstance(parameter_count, int):
        raise ValueError("parameter_count must be a whole number")
    if parameter_count <= 0:
        raise ValueError("parameter_count must be greater than zero")

    if not isinstance(precision, str):
        raise ValueError("precision must be a text format name")
    normalized_precision = precision.lower()
    if normalized_precision not in BITS_PER_PARAMETER:
        choices = ", ".join(BITS_PER_PARAMETER)
        raise ValueError(f"precision must be one of: {choices}")

    # Convert bits to bytes, then bytes to decimal gigabytes.
    bits_per_parameter = BITS_PER_PARAMETER[normalized_precision]
    bytes_needed = parameter_count * bits_per_parameter / 8
    return bytes_needed / 1_000_000_000


def main() -> int:
    """Read model details from the command line and print an estimate."""
    # argparse reads and checks the two values typed after the command.
    parser = argparse.ArgumentParser(
        description="Estimate memory needed to store AI model parameters."
    )
    parser.add_argument(
        "parameter_count",
        type=int,
        help="number of model parameters, for example 7000000000",
    )
    parser.add_argument(
        "precision",
        type=str.lower,
        choices=tuple(BITS_PER_PARAMETER),
        help="number format used to store each parameter",
    )
    args = parser.parse_args()

    try:
        memory_gb = estimate_memory_gb(args.parameter_count, args.precision)
    except ValueError as error:
        parser.error(str(error))

    print(
        f"Estimated parameter memory: {memory_gb:.2f} GB "
        f"({args.precision}, {args.parameter_count:,} parameters)"
    )
    print("This covers parameter storage only; running a model needs additional memory.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
