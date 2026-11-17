import pytest

from ailab.model_size import estimate_memory_gb


@pytest.mark.parametrize(
    ("precision", "expected_gb"),
    [("fp32", 28.0), ("fp16", 14.0), ("bf16", 14.0), ("int8", 7.0), ("int4", 3.5)],
)
def test_estimate_memory_for_supported_formats(precision, expected_gb):
    assert estimate_memory_gb(7_000_000_000, precision) == expected_gb


def test_precision_is_case_insensitive():
    assert estimate_memory_gb(1_000_000_000, "FP16") == 2.0


@pytest.mark.parametrize("invalid_count", [0, -1, 1.5, "100", True])
def test_parameter_count_must_be_positive_integer(invalid_count):
    with pytest.raises(ValueError):
        estimate_memory_gb(invalid_count, "fp16")


def test_unknown_precision_is_rejected():
    with pytest.raises(ValueError, match="precision must be one of"):
        estimate_memory_gb(100, "fp64")


def test_precision_must_be_text():
    with pytest.raises(ValueError, match="text format name"):
        estimate_memory_gb(100, None)
