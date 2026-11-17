# Troubleshooting

## Setup and Python

### `python3` or the selected Python command was not found

Install Python 3.10 or newer, then check which command works on your computer:

```sh
python3 --version
python --version
```

On Windows, the Python launcher can select an installed version:

```powershell
py -3.12 --version
```

For the setup script, select a specific Unix-like Python command with `make setup PYTHON=python3.12`.

### Creating the virtual environment fails

Make sure the selected Python installation includes its `venv` module. On Linux distributions, the module may be packaged separately from the base Python installation. Use the installation instructions for your operating system, then rerun `make setup`.

### `make check` says `.venv/bin/python` does not exist

Run setup from the project root first:

```sh
make setup
```

The Makefile uses the environment at `.venv`. On Windows, follow the PowerShell setup commands in the README and run tools with `\.venv\Scripts\python.exe -m ailab.check_env`.

### `No module named ailab`

Install the project into the virtual environment from the project root:

```sh
make setup
```

The setup script performs an editable install, which tells Python where the project's `src/ailab/` package lives.

### Package installation fails

The first install needs access to the Python package index. Check your network connection and rerun setup. If a package download was interrupted, rerunning `make setup` is safe; pip can continue installing missing packages.

## Readiness check

### The check reports that no virtual environment is active

The Makefile invokes `.venv/bin/python` directly, so `make check` should report the project's environment as active. If you run the module with another Python command, activate `.venv` first or use its interpreter directly.

### `nvidia-smi` is not found or cannot query a GPU

This is an informational result. The checker only asks NVIDIA's `nvidia-smi` tool for GPU details. It does not report free VRAM, and it does not identify AMD, Apple, or other non-NVIDIA GPUs. The rest of the readiness checks can still be useful without an NVIDIA GPU.

## Model memory estimate

### The estimate is smaller than the model file or the model still does not fit

`model_size.py` estimates parameter storage from the parameter count and number format. It does not inspect a downloaded file, include file metadata, or account for memory used by temporary calculations, prompts, or a language-model KV cache. Treat it as a first estimate, not a guarantee that the model will run.

### The command rejects a parameter count or format

Use a positive whole-number parameter count and one supported format: `fp32`, `fp16`, `bf16`, `int8`, or `int4`.

```sh
make estimate PARAMETERS=7000000000 PRECISION=fp16
```

## Benchmark and report

### The benchmark feels slow or uses too much memory

The default benchmark multiplies two 512-by-512 matrices five times. Try a smaller size and fewer repetitions:

```sh
.venv/bin/python -m ailab.benchmark --size 128 --repetitions 2
```

The benchmark uses NumPy and does not select a GPU. Its `local` or `colab` label describes where you ran the command.

### The notebook cannot find a result file

The report notebook expects both `results/local_benchmark.json` and `results/colab_benchmark.json`, and expects its current working directory to be the project root. Run the benchmark once in each environment and copy the Colab result file into the project's `results/` folder before comparing.

### The report says the runs are not directly comparable

The report only compares runs with the same matrix size and data type. Rerun both environments with matching `--size` and `float32` settings. Different hardware and system load can still produce different timings.

### The JSON file is empty or invalid

An empty placeholder file is not a benchmark result. Rerun the benchmark for that environment to write valid JSON, then rerun the notebook cells.

## Tests

### `make test` succeeds but a feature is still broken

Some test files are empty and the logging tests still contain placeholder assertions. The current suite does not cover every behavior. Treat this as known incomplete coverage and add meaningful tests as each feature is completed.
