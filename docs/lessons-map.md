# Lessons Map

This map connects the current tools with the concepts they teach. The repository is a learning toolkit; some later application-building lessons are planned in [Build and Ship: Hands-on Learning Path](build-and-ship-learning-path.md).

## Current toolkit

| Lesson | Project files | What to practice | What you should be able to explain |
|---|---|---|---|
| Project setup and settings | `pyproject.toml`, `.env.example`, `src/ailab/config.py` | Create `.venv`, install the package, load defaults, and retrieve a required key | Required versus optional dependencies; configuration versus secrets; why `.env` stays local |
| Logging | `src/ailab/logging_setup.py`, `tests/test_logging_setup.py` | Configure a level and optionally write a log file | What a log record is and how levels filter messages |
| Machine readiness | `src/ailab/check_env.py` | Run `make check` and interpret each status | Python version, active virtual environment, package imports, Git availability, system RAM, NVIDIA VRAM, and GPU vendor limits |
| Model memory estimate | `src/ailab/model_size.py`, `tests/test_model_size.py` | Compare `fp32`, `fp16`, `bf16`, `int8`, and `int4` estimates | How parameter count and bits per parameter estimate weight storage, and why runtime memory is higher |
| Performance benchmark | `src/ailab/benchmark.py` | Run a small benchmark, change its size/repetitions, and inspect its JSON | Matrix multiplication timing, warm-up, repeated measurements, seeds, and why the current NumPy benchmark does not choose a GPU |
| Compare results | `notebooks/report.ipynb` | Load local and Colab JSON files and compare compatible runs | Why matrix size and data type need to match, and why a timing is tied to the machine and software environment |
| Sample data | `scripts/download_sample_data.py`, `data/` | Download a small public file over HTTPS and inspect the ignored output | Streaming, size limits, safe filenames, temporary files, and why downloaded data is not automatically committed |

## Practical learning sequence

1. Follow the README setup steps and explain what `.venv` and editable installation do.
2. Run the readiness check and describe which results are pass, warning, or information.
3. Calculate one model-size example by hand, then compare it with the command output.
4. Run a small benchmark, open the JSON, and identify its inputs, environment details, and timing fields.
5. Compare two runs in the notebook and explain what makes the comparison fair or unfair.
6. Read the focused tests to see how behavior is checked, then run them with `make test` when you are ready to verify a change.
7. When ready, continue into the frontend, API, database, AI integration, and deployment activities in the hands-on learning path.

## Completion note

The test suite covers the current core behaviors, but passing tests do not guarantee that every operating system, GPU, network server, or deployment will behave identically. Inspect the relevant tests and run them in the environment you intend to use.
