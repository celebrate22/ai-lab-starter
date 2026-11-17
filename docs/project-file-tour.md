# Project File Tour: Plain-English Guide

This guide explains what the main files do, why they exist, and how they fit together. You do not need to memorize every file. Start with the setup flow, then follow a tool from its input to its output.

## The project in one picture

```text
pyproject.toml  -> tells Python how to install the project and its packages
scripts/setup.sh -> creates .venv and installs the project
src/ailab/       -> the Python tools you can run
tests/           -> examples that check those tools' behavior
benchmark.py     -> creates a result JSON file in results/
report.ipynb     -> reads the JSON files and compares the numbers
```

Think of the repository like a small workshop: `src/` contains the tools, setup files prepare the workshop, tests check the tools, and `results/` stores measurements made by using them.

## Run a command from start to finish

For example, when you type:

```sh
make estimate
```

1. `make` looks for a target named `estimate` in `Makefile`.
2. That target runs `.venv/bin/python -m ailab.model_size 7000000000 fp16`.
3. Python finds the installed `ailab` package and runs `model_size.py`.
4. The module checks the two inputs, does the calculation, and prints the answer.

`benchmark` follows a similar path, then saves its output to a JSON file. The notebook later reads that file; it does not run the benchmark itself.

## The main Python tools

### `src/ailab/model_size.py`

This tool answers: “How much memory would it take just to store this many model parameters in this number format?” It does not open a model, read a prompt, count tokens, or check your computer's actual RAM or VRAM.

It keeps a small table of format sizes: `fp32` uses 32 bits per parameter, `fp16` and `bf16` use 16, `int8` uses 8, and `int4` uses 4. It then does:

```text
bytes = parameter count * bits per parameter / 8
decimal GB = bytes / 1,000,000,000
```

Example: 7 billion parameters at 16 bits each use `7,000,000,000 * 16 / 8` = 14 billion bytes, or about 14 GB for the weights alone. A real running model also needs working memory, so this estimate is not a promise that it will fit.

The command:

```sh
make estimate PARAMETERS=7000000000 PRECISION=fp16
```

passes those two values through Make to the Python program. `argparse` reads them and reports a helpful error if they are invalid.

### `src/ailab/benchmark.py`

This tool answers: “How long does this Python environment take to multiply two number grids?” A number grid is called a matrix. The benchmark creates two random square matrices, multiplies them using NumPy, and times the multiplication several times.

The first multiplication is a warm-up and is not included in the reported times. The code then records each timed run, calculates the average and fastest time, and saves settings and measurements as JSON. It records details like matrix size, random seed, Python version, NumPy version, and operating system so you can understand what machine produced the timings.

It is a basic CPU-oriented NumPy measurement: it does not ask for or select a GPU. `--environment local` or `--environment colab` is only a label you choose. The maximum matrix edge is limited to 4096 to help prevent accidental large memory use.

Try a small run:

```sh
.venv/bin/python -m ailab.benchmark --size 128 --repetitions 2
```

`--size 128` means each input has 128 rows and 128 columns. `--repetitions 2` asks for two timed multiplications after warm-up.

### `src/ailab/logging_setup.py`

Logging is a way for a program to leave a readable trail of what happened. It is like `print()`, but messages have a time and an importance level, and they can be saved to a file.

`setup_logging("INFO")` sends messages to the terminal. `setup_logging("INFO", "run.log")` sends them to the terminal and to `run.log`. The output format is timestamp, level, then message. Common levels, from less serious to more serious, are `DEBUG`, `INFO`, `WARNING`, `ERROR`, and `CRITICAL`. With level `INFO`, informational and more serious messages appear; debug messages are hidden.

Example use in Python:

```python
import logging
from ailab.logging_setup import setup_logging

setup_logging("INFO", "run.log")
logging.info("Starting the benchmark")
logging.error("The input file could not be read")
```

The logging setup only configures logging. A tool must call `logging.info(...)` or another logging function to create messages. At the moment, it is a reusable foundation; it does not automatically make every project tool log its actions.

### `src/ailab/config.py` and `.env` files

Configuration means values that let the same code behave differently without editing the code. For example, `LOG_LEVEL=DEBUG` asks for more detailed messages, while `DATA_DIR=data` names a folder.

`load_settings()` asks `python-dotenv` to read a local `.env` file, then returns `LOG_LEVEL` and `DATA_DIR`, using `INFO` and `data` if they are not set. `get_key("OPENAI_API_KEY")` looks up an API key and gives a clear error if it is missing. This project provides the lookup mechanism, but it does not currently call an AI provider with that key.

`.env.example` is a sample list of setting names. Copy it to `.env` and put real private values only in your local `.env`. Git ignores `.env` because it may contain passwords or API keys. The example file contains blank key values, not working API keys.

### `src/ailab/check_env.py`

This is the readiness checklist. It checks the Python version, whether a virtual environment appears active, whether Git is available, whether required Python packages can be imported, and whether NVIDIA's `nvidia-smi` command can report a GPU. It does not measure GPU memory capacity.

## Setup and project configuration files

### `scripts/setup.sh`

This is a small shell script that performs project setup on Linux or macOS. Read it from top to bottom:

1. `#!/bin/sh` says to run the file with a basic Unix shell.
2. `set -eu` makes the script stop when a command fails or when it tries to use a missing variable. That avoids continuing with a half-finished setup.
3. `PROJECT_ROOT=...` finds the project folder based on where this script lives. This means it can be run from another current folder too.
4. `cd "$PROJECT_ROOT"` moves into the project folder before creating files.
5. `PYTHON=${PYTHON:-python3}` uses a provided `PYTHON` command if one exists; otherwise it uses `python3`.
6. `command -v` checks that the selected Python command can be found.
7. `python -m venv .venv` creates a private Python installation for this project in `.venv/`.
8. `.venv/bin/python -m pip install -e '.[dev]'` installs this project into that environment, plus its development tools. The `-e` means editable: Python uses the source files in this folder, so code edits do not require reinstalling.
9. The final `echo` prints what to do next.

You can run the same setup using `make setup`. On Windows, the README gives PowerShell commands because this shell script uses Unix shell syntax.

### `pyproject.toml` and `.toml`

TOML is a plain-text format for settings: section names go in square brackets and values are written as `name = value`. It is data, not Python code.

In this project's `pyproject.toml`:

- `[project]` names the package, supported Python version, and packages needed for normal use (`numpy` and `python-dotenv`).
- `[project.optional-dependencies]` lists tools used for extra work. The `dev` group adds `pytest` for tests and `jupyter` for notebooks.
- `[build-system]` tells pip which packaging tool builds/installs the project.
- `[tool.setuptools.packages.find]` tells that tool to find Python packages under `src/`.

The dependency lists are instructions to pip; they are not the actual installed packages. `pip install -e '.[dev]'` reads this TOML file and installs them into `.venv`.

### `requirements.txt`

This file is usually a list of packages for pip to install. Here it only contains comments explaining that `pyproject.toml` is the real source of dependency lists. It is intentionally not a second dependency list, which could drift out of sync. So `requirements.txt` itself installs nothing; use the setup command from the README.

### `Makefile`

A Makefile provides short names for longer terminal commands. Each named action is called a target. For example, `make check` is a shortcut for running the readiness check with the project's `.venv` Python. `make test`, `make estimate`, and `make benchmark` are other shortcuts.

Values such as `PARAMETERS ?= 7000000000` are defaults. The `?=` means “use this value unless the person running Make supplied another one.” Thus `make estimate PARAMETERS=1000000000 PRECISION=fp32` changes the inputs for that run.

### `LICENSE`

This file is currently empty. That means the repository does not currently state a license that grants others permission to reuse, change, or redistribute the code. It is not the same as a license saying “do anything.” The project owner needs to choose a license before inviting reuse; this guide does not choose one for them.

### `Dockerfile` and `.dockerignore`

The `Dockerfile` is a recipe for building a Docker image: a packaged environment containing Python and this project. The image starts by running the environment check.

`.dockerignore` is a list of files Docker should leave out while it prepares files for the image build. This project excludes `.git`, `.venv`, caches, `.env*`, downloaded data, and benchmark JSON files. This makes the build smaller and helps keep private settings out of the image. It only affects Docker builds; it does not delete those files from your computer. `.gitignore` is a separate list for Git.

## Folders, generated files, and saved results

### `src/ailab/` and the name `ailab`

`src/` is where the project's reusable Python package lives. `ailab` is the package name from `pyproject.toml`; a module can be run as `python -m ailab.model_size`. The importable package name is `ailab`, even though the project folder is called `ai-lab-starter`.

### `scripts/`

Scripts are helper programs for one-off tasks around the package. `setup.sh` prepares the environment. `download_sample_data.py` downloads one public sample file into `data/`. The core tools live in `src/ailab/` because other Python code may import and reuse them.

### `src/ailab.egg-info/`

This folder is generated by the Python packaging/install process. It contains installation notes such as the package name, version, and dependency list. It is not source code and should not be hand-edited; a later package installation can regenerate it. Git ignores `*.egg-info/` for that reason.

### `results/` and the JSON files

JSON is a plain-text way to save named values. The benchmark saves the settings and times from one run as JSON. `local_benchmark.json` is meant for a run made on your computer; `colab_benchmark.json` is meant for a run made in Colab. They let the report compare measurements later.

The two files currently in the repository are empty starter placeholders, not completed measurements. Run the benchmark in each environment to create real contents. The notebook cannot compare empty files. `.dockerignore` excludes these results from Docker images. `.gitignore` ignores newly created result JSON files, but these two empty files are already tracked by Git; until they are untracked, changes to them will still appear in Git.

### `notebooks/report.ipynb`

An `.ipynb` file is a Jupyter notebook. It combines explanation (text cells) and runnable Python (code cells). This notebook opens the local and Colab JSON result files, checks that the matrix sizes and number formats match, and displays their average times. It does not run the benchmark or create either result file.

The notebook runs code in a **kernel**, which is the Python process behind the notebook. Run cells from top to bottom: the first code cell loads the result dictionaries into variables, and the next cell uses those variables to compare times.

## Other useful files

- `.gitignore` tells Git which local or generated files not to include when tracking changes. It differs from `.dockerignore`, which only filters Docker build input.
- `.env.example` lists setting names to copy into a private `.env` file.
- `tests/` contains automated checks; the tests use fake inputs for the downloader, so tests do not need to download real files.
- `docs/` contains learning and troubleshooting guides. `AGENTS.md` keeps the project's shared concept notes.
- `data/.gitkeep` is a tiny tracked file that makes Git retain the otherwise empty `data/` folder. Downloaded data files in that folder are ignored.

## A practical order to learn this project

1. Read `pyproject.toml` to see the package name and dependencies.
2. Follow `scripts/setup.sh` and identify which step creates `.venv` and which step installs packages.
3. Run `make check` and connect the output to `check_env.py`.
4. Run `make estimate` and trace the inputs to the memory formula in `model_size.py`.
5. Run a small benchmark and inspect the JSON fields it creates.
6. Open the notebook and follow how it reads those fields and compares the two averages.
7. Read `logging_setup.py` and try adding one `logging.info(...)` call to a tool when you are ready to see logging in action.
