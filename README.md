# AI Lab Starter

`ai-lab-starter` is a small Python toolkit for checking whether a computer is ready for AI experiments, estimating model-weight memory, and measuring a basic matrix-multiplication workload.

If the files and terms are new, start with the [plain-English project file tour](docs/project-file-tour.md). It explains the setup script, configuration, benchmark flow, generated results, and notebook.

It helps answer four questions:

1. **Is my Python setup ready?** `check_env.py` checks the Python version, virtual environment, Git command, required package imports, and whether NVIDIA's `nvidia-smi` tool can report a GPU.
2. **How much memory might model weights need?** `model_size.py` estimates parameter storage from a parameter count and number format.
3. **How quickly does this machine multiply matrices?** `benchmark.py` measures NumPy matrix multiplication and saves settings and timings as JSON.
4. **How do local and Colab measurements compare?** `notebooks/report.ipynb` reads the saved JSON files and compares compatible runs.

## Requirements

- Python 3.10 or newer
- `make` and a POSIX-compatible shell to use the Makefile and setup script (Linux and macOS provide these commonly)
- An internet connection for the initial package installation

On Windows, use the PowerShell commands below instead of the Makefile setup path.

## Setup

On Linux or macOS, from the project root run:

```sh
make setup
```

This creates `.venv`, an isolated Python environment for this project, and installs the project plus its development tools. If your Python command is named differently, provide it to Make, for example:

```sh
make setup PYTHON=python3.12
```

PowerShell setup:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

The commands below use the `.venv` Python directly, so you do not need to activate the environment first.

## Run the tools

Check the environment:

```sh
make check
```

Estimate memory for 7 billion parameters stored in `fp16`:

```sh
make estimate
```

Choose different inputs:

```sh
make estimate PARAMETERS=13000000000 PRECISION=fp16
```

Run the benchmark and save a local result to `results/local_benchmark.json`:

```sh
make benchmark
```

On a copy of the project running in Colab, label the output as Colab so it is saved to `results/colab_benchmark.json`:

```sh
make benchmark ENVIRONMENT=colab
```

Open the comparison notebook from the project root:

```sh
.venv/bin/jupyter notebook notebooks/report.ipynb
```

Run the tests:

```sh
make test
```

The tests cover the current checks, configuration, logging, estimates, benchmark input validation, and the sample-data downloader. They do not prove behavior on every operating system or hardware setup.

## Download a small sample file

The helper accepts an HTTPS URL, writes into `data/`, and limits downloads to 10 MB by default. It does not choose or download a file automatically; use a public sample URL you trust:

```sh
.venv/bin/python scripts/download_sample_data.py https://example.org/sample.csv
```

Choose a filename or change the size limit when needed:

```sh
.venv/bin/python scripts/download_sample_data.py https://example.org/sample.csv --filename tiny.csv --max-mb 2
```

An existing file is preserved unless `--force` is supplied. `data/` contents are ignored by Git so downloaded data is not accidentally added to project history.

## Important limits

- The model-size result estimates storage for weights only. It does not inspect a model file or available RAM/VRAM, and it excludes memory needed while the model runs.
- The environment check can ask `nvidia-smi` about NVIDIA hardware; it does not measure free GPU memory or check every GPU vendor.
- The benchmark uses NumPy and does not select a GPU. It measures the NumPy matrix-multiplication implementation available in that environment, normally on the CPU. The `local` and `colab` labels describe where you ran it; they do not configure the hardware.
- The benchmark limits each matrix edge to 4096 elements to reduce accidental large allocations. This still uses about 192 MiB for its two inputs and one output at maximum size, before NumPy backend workspace.
- For a fair timing comparison, use the same matrix size and data type on both machines. Different hardware, system load, and NumPy builds can still affect results.

## Run with Docker

Build the image and run the readiness check:

```sh
make docker-check
```

Or build and run in separate steps:

```sh
make docker-build
docker run --rm ai-lab-starter
```

The image runs `ailab.check_env` by default. To run a different module, add its name and arguments after the image name:

```sh
docker run --rm ai-lab-starter ailab.model_size 7000000000 fp16
```

The container has its own filesystem and does not automatically see your host's GPU or `.env` file. This minimal image does not include `nvidia-smi`, so its GPU check reports that NVIDIA status is unavailable. A GPU-enabled container would need both NVIDIA tooling in the image and compatible runtime configuration. Never copy real secrets into the image; pass them through a secure runtime configuration only when a tool needs them. Benchmark result files created in a disposable container are removed when it exits unless you mount a host folder for them.

## Project map

- `src/ailab/check_env.py` — machine readiness checks
- `src/ailab/config.py` — settings and API-key lookup
- `src/ailab/logging_setup.py` — terminal and optional file logging
- `src/ailab/model_size.py` — parameter-memory estimate
- `src/ailab/benchmark.py` — matrix-multiplication timing and JSON output
- `scripts/download_sample_data.py` — download a bounded public sample file into `data/`
- `notebooks/report.ipynb` — compare local and Colab benchmark files
- `tests/` — automated behavior checks
- `docs/build-and-ship-learning-path.md` — practical path from this toolkit to a deployed application
