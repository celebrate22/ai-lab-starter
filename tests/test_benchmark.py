import pytest

from ailab.benchmark import MAX_MATRIX_SIZE, run_benchmark


def test_run_benchmark_returns_measurements():
    result = run_benchmark(matrix_size=4, repetitions=2, seed=7)
    assert result["matrix_size"] == 4
    assert result["repetitions"] == 2
    assert result["seed"] == 7
    assert len(result["durations_seconds"]) == 2
    assert all(duration >= 0 for duration in result["durations_seconds"])
    assert result["average_seconds"] == sum(result["durations_seconds"]) / 2


@pytest.mark.parametrize(
    ("arguments", "message"),
    [
        ({"matrix_size": 0}, "greater than zero"),
        ({"matrix_size": MAX_MATRIX_SIZE + 1}, "cannot be greater"),
        ({"matrix_size": True}, "whole number"),
        ({"repetitions": 0}, "greater than zero"),
        ({"repetitions": 1.5}, "whole number"),
        ({"seed": -1}, "cannot be negative"),
        ({"seed": True}, "whole number"),
    ],
)
def test_run_benchmark_rejects_invalid_inputs(arguments, message):
    with pytest.raises(ValueError, match=message):
        run_benchmark(**arguments)
