# Project Concepts

These notes explain concepts already present in this project. Add a short definition and a project-specific example whenever a new concept comes up.

### AI lab purpose and measurements

- **Machine readiness check:** A program that checks whether a computer has the basic software and hardware needed for a task. `check_env.py` is intended to report items such as the Python version, whether required packages import correctly, and whether an NVIDIA GPU is available.
- **Virtual environment:** An isolated Python setup for one project, so installed packages for one project do not interfere with another. Python detects an active virtual environment when `sys.prefix` differs from `sys.base_prefix`; the readiness check recommends one but does not fail if it is absent.
- **Import:** Loading a Python module so the program can use its code. The readiness check tries to import `numpy` and `dotenv`, which correspond to the project's `numpy` and `python-dotenv` dependencies.
- **Command-line interface (CLI):** A way to run a program by typing a command in a terminal. `python -m ailab.check_env` asks Python to run the `check_env` module as a program.
- **PATH:** A list of folders the operating system searches when a command is run by name. The readiness check uses it to see whether commands such as `git` and `nvidia-smi` are available.
- **Subprocess:** A separate program started by Python. `check_env.py` starts `nvidia-smi` as a subprocess to ask NVIDIA's tool for GPU information.
- **Exit code:** A number a program returns when it finishes. Zero usually means success; a nonzero number signals a problem. The readiness check returns a nonzero code when Python is too old or a required package cannot be imported.
- **Timeout:** A limit on how long an operation may take. The GPU query has a five-second timeout so a stuck system command cannot hang the check indefinitely.
- **Model parameter:** A learned number inside an AI model. The number of parameters is one rough measure of model size. For example, a model with 7 billion parameters has 7 billion learned numbers.
- **Number format / precision:** The way each number is stored, including how many bits are used. `fp16` stores each number in 16 bits; lower precision generally uses less memory, though it can affect numerical accuracy.
- **Memory estimate:** An approximate calculation of how much memory is needed to store model parameters. For parameter storage alone, 7 billion parameters at 16 bits each need about 14 billion bytes (roughly 14 GB in the project's simplified estimate). Real model use also needs memory for other data, so the estimate is not a guarantee that a model will run.
- **VRAM:** Memory on a graphics processing unit (GPU). AI models and calculations running on the GPU need enough VRAM for the model and its working data. A model estimate larger than available VRAM is a warning that it may not fit.
- **Benchmark:** A timed workload used to measure and compare performance. `benchmark.py` is intended to time matrix multiplication on the local computer and in Google Colab.
- **Matrix multiplication:** A mathematical operation combining rows and columns of number tables (matrices). It is a common workload in AI, so its speed can give a rough view of compute performance.
- **Google Colab:** A hosted notebook service where code can run on a remote computer, sometimes with a GPU. Comparing local and Colab benchmark results compares different machines; results depend on the hardware and setup used for each run.
- **JSON:** A plain-text format for storing structured data as named fields and lists. The benchmark results are intended to be saved as JSON files, such as `local_benchmark.json` and `colab_benchmark.json`.
- **Reproducibility:** The ability for another person to repeat an experiment and understand how its result was produced. Clear setup steps, recorded settings, and saved benchmark results help make this possible, though different hardware can still produce different timings.

### Project files and Python

- **File extension:** The ending of a filename, such as `.py` or `.toml`. It usually hints at the file's format or purpose.
- **TOML (`.toml`):** A readable text format for configuration, meaning settings that describe how a program or tool should behave. This project's `pyproject.toml` describes the Python project, its dependencies, and its build setup. TOML uses sections in square brackets and key/value pairs.
- **Python package:** A collection of Python code that can be imported and reused. This project puts its package code in `src/ailab/`; for example, `ailab.config` refers to the `config.py` module inside the `ailab` package.
- **Module:** A Python file that groups related code and can be imported by other Python files. For example, `config.py` is a module.
- **Dependency:** Code or a tool that this project relies on but does not provide itself. Required dependencies are installed for the project's normal use. `numpy` and `python-dotenv` are listed as required dependencies in `pyproject.toml`.
- **Optional dependency:** An extra dependency needed only for certain activities, not for every use of the project. The `dev` group lists `pytest` for running tests and `jupyter` for working with notebooks.
- **Build system:** The tools and instructions used to package or install a Python project. The `[build-system]` section of `pyproject.toml` specifies setuptools for this project.
- **Standard library:** Python modules included with Python itself, so they do not need to be installed separately. `check_env.py` uses standard-library modules such as `sys`, `shutil`, and `subprocess`.
- **Import statement:** A line that makes code from a module available in the current file. For example, `import sys` lets `check_env.py` use Python's version and environment details.
- **`dataclasses`:** A Python standard-library module for creating simple classes that hold related values. `from dataclasses import dataclass` brings its `dataclass` helper into `check_env.py` so it can define `CheckResult` concisely.
- **`importlib`:** A Python standard-library module for working with imports programmatically. `importlib.import_module(module_name)` lets the readiness check try to import a package whose name is given as text.
- **`shutil`:** A Python standard-library module with file and system utilities. `shutil.which("git")` and `shutil.which("nvidia-smi")` look for those commands in the system's PATH.
- **`subprocess`:** A Python standard-library module for starting other programs. `subprocess.run()` starts `nvidia-smi` and captures its response.
- **`sys`:** A Python standard-library module with information about the running Python process. `sys.version_info` gives its version; `sys.prefix` and `sys.base_prefix` help identify an active virtual environment.
- **Captured output:** Text that a program saves instead of immediately showing in the terminal. The GPU check captures `nvidia-smi` output in `result.stdout` so it can print the GPU name.
- **Standard output (`stdout`):** The normal text output of a command-line program. The readiness check reads the GPU name from the `stdout` returned by `subprocess.run()`.
- **Function:** A named block of code that can be called to do a task. `check_python()` is a function that checks the running Python version and returns a result.
- **Parameter:** A named input listed in a function definition. `module_name` is the parameter to `check_package()`, allowing it to check different modules.
- **Return value:** The value a function gives back to the code that called it. Each readiness check returns a `CheckResult` object.
- **Type hint:** A note in Python code describing the expected kind of a value; Python generally does not enforce it at runtime. `check_python() -> CheckResult` says the function is expected to return a `CheckResult`.
- **Dataclass:** A class for holding related data, with Python generating common methods such as its initializer. `CheckResult` groups a status and message.
- **Frozen dataclass:** A dataclass whose fields cannot be reassigned after creation. `@dataclass(frozen=True)` prevents a check result's `status` or `message` from being changed later.
- **Docstring:** A string immediately inside a module, class, or function that describes its purpose. The first line of `check_env.py` describes the module, and functions have short docstrings too.
- **Conditional:** Code that chooses what to do based on whether a condition is true. `if version >= (3, 10)` selects the success or error result.
- **Tuple:** An ordered collection of values, commonly used for a fixed group. `sys.version_info` and `(3, 10)` are compared to decide whether Python meets the minimum version.
- **F-string:** A string prefixed with `f` that can insert values inside braces. `f"Python {version.major}..."` builds a readable version message.
- **Exception handling:** Code that responds to an error raised while an operation runs. `try` and `except ImportError` let `check_package()` report a missing or broken import instead of stopping the program.
- **List:** An ordered collection that can hold multiple values. `run_checks()` returns a list of `CheckResult` objects, and the subprocess command is passed as a list of words.
- **Boolean:** A value that is either `True` or `False`. `shutil.which()` returns a path when a command is found and `None` when it is not; `if` treats these as true and false.
- **Subprocess result:** The information returned after Python runs another program, including its output and exit status. `subprocess.run()` returns a result whose `stdout` contains `nvidia-smi`'s response.
- **Keyword argument:** An input passed to a function by naming the setting as well as its value. In `subprocess.run(..., timeout=5)`, `timeout` is a keyword argument that sets the time limit.
- **String method:** An operation provided by a string value. `strip()` removes surrounding whitespace, while `splitlines()` separates output into lines.
- **Indexing:** Selecting an item by its position; Python starts counting positions at zero. `gpu_names.splitlines()[0]` selects the first reported GPU name.
- **Loop:** Code that repeats for each item in a collection. `for result in results` prints one line for each readiness check.
- **Built-in function:** A function Python provides without an import. `print()` displays results, `any()` checks whether at least one item is true, and `int()` converts a Boolean to `1` or `0`.
- **Module entry-point guard:** `if __name__ == "__main__":` checks whether a Python file was run directly as a program. In this module it starts `main()` only for direct execution, not when imported.
- **SystemExit:** Python's mechanism for ending a program with a chosen exit code. `raise SystemExit(main())` ends the command-line run using the code returned by `main()`.

### Configuration and secrets

- **Configuration:** Settings that control how a program runs without changing its main code. Examples here include the log level and data folder.
- **Setting:** One individual configuration value, such as `LOG_LEVEL=INFO`.
- **Environment variable:** A named value made available to a program by its environment. It can hold an ordinary setting or a secret. `config.py` reads `LOG_LEVEL` and `DATA_DIR` as settings, and uses defaults when those values are absent. `get_key()` retrieves a required value such as an API key.
- **`.env` file:** A text file used during development to supply environment variables. Here, `python-dotenv` reads it. It is called local because each developer keeps their own copy on their computer rather than sharing personal values in the project repository. It may contain secrets, so Git is configured to ignore it.
- **`.env.example` file:** A safe example showing which environment variables a developer may need to set. It is a template to copy and fill in; its blank API key values are not working keys.
- **Template:** A starting example that someone copies and customizes. In this project, `.env.example` is the template for a personal `.env` file.
- **API key:** A private credential that identifies or authorizes an application when it connects to a service through an Application Programming Interface (API). It works somewhat like a password. If exposed, someone else may use the account or service, consume its usage limits, cause charges, or access data allowed by that key.
- **Secret:** Private information that could let someone access an account or service, such as an API key or password. An ordinary setting like `LOG_LEVEL=INFO` is not usually a secret: it controls program behavior but does not grant access. Keep secrets out of source code, screenshots, logs, and Git history.
- **Default value:** A fallback used when no explicit setting is provided. `load_settings()` defaults `LOG_LEVEL` to `INFO` and `DATA_DIR` to `data`.
- **Immutable settings object:** `Settings` is a frozen dataclass, which means its values are grouped into one object and cannot be reassigned after creation. This helps avoid accidental configuration changes while the program runs.

### Git and project history

- **Git:** A version control tool that records changes to files over time so developers can review, compare, and share project history.
- **Repository:** A project folder tracked by Git, including its files and recorded history.
- **Working tree:** The current files in the project folder, including edits not yet saved in a Git commit.
- **Diff:** A readable view of changes between versions of files. It helps review exactly what was added, removed, or edited.
- **Staging area:** A place in Git where selected changes are prepared for the next commit. The `git add` command stages changes. Staging lets a developer choose which edits belong together in one commit.
- **Commit:** A named snapshot of the staged project changes saved in Git history. The usual flow is to review the diff, stage selected changes, and commit them.
- **Push:** Sending local commits to a shared remote repository so others can access them. A push shares committed work; it does not stage or create a commit.
- **`.gitignore`:** A file listing paths Git should generally leave untracked. This project uses it to exclude local `.env` files and generated data while keeping `.env.example` and `data/.gitkeep` tracked.
- **Remote repository:** A copy of the Git repository hosted elsewhere, such as on a code hosting service. `origin` is the conventional name for this project's remote.

### Tests and tools

- **Test:** Code that checks whether other code behaves as expected. For example, `tests/test_config.py` checks that missing keys cause an error and defaults are used when settings are absent.
- **pytest:** A Python tool for finding and running tests. It is listed as a development dependency in this project.
- **Fixture:** Reusable setup or cleanup provided to tests. The `restore_logging` fixture saves the logger's state before each test and restores it afterward.
- **Mocking:** Replacing or controlling part of a program during a test so the test can check a specific situation. The configuration tests use pytest's `monkeypatch` to set or remove environment variables temporarily.
- **Placeholder:** Incomplete code or text marking something to fill in later. The `...` assertions in `tests/test_logging_setup.py` are placeholders, so those tests are not finished yet.
- **Logger:** A program component that records messages about what the program is doing. This project's `setup_logging()` configures messages to go to the terminal and optionally to a file.
- **Log level:** A label that indicates the importance of a log message, such as `DEBUG`, `INFO`, or `ERROR`. A level controls which messages are shown.

### As the project grows

Add concepts such as command-line tools, shell scripts, notebooks, data files, benchmarks, containers, model files, or deployment when they come up. Include a concise definition and an example from this project.
