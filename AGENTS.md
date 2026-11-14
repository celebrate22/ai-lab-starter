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
- **Model parameter:** A number adjusted during training so an AI model can learn patterns. A model may have millions or billions of parameters. We count them because each stored parameter uses memory; multiplying the count by the bits used for each number estimates the memory needed to store the model's parameters. For example, 7 billion parameters stored at 16 bits each need about 14 GB for parameter storage alone.
- **Model weights:** Another common name for the learned parameter values in a model. When a model is loaded, its weights must be placed in memory before it can make predictions.
- **AI model:** A computer program made from a design (its architecture) and, for a trained model, learned parameter values. It uses the design and values to turn an input into a prediction or response.
- **Architecture:** The arrangement of parts and operations that defines how a model processes information. Two models can have different architectures even when they have similar parameter counts.
- **Training data:** Examples used to teach a model, such as text the model learns patterns from. Training data is used during training and is not counted as model parameters.
- **Training:** The process of adjusting a model's parameters using examples so its predictions improve. Training typically uses more memory than just storing the finished weights.
- **Loss:** A number that measures how far a model's prediction is from the desired answer during training. Training tries to reduce this error measure.
- **Optimizer:** A training method that uses the loss to decide how to adjust model parameters. Optimizer state takes additional memory during training.
- **Layer:** One processing stage in a neural network. A language model passes numeric information through many layers to produce its next-token prediction.
- **Forward pass:** One run of input through a model's layers to calculate a prediction. During a prompt response, the model performs forward computations to predict the next token.
- **Logit:** A raw score the model produces for each possible next token before those scores are converted into probabilities.
- **Probability distribution:** A set of probabilities over possible next tokens. The model uses these probabilities to choose or sample a next token.
- **Autoregressive generation:** Producing text one token at a time, feeding each generated token back as context to predict the next one.
- **Context window:** The maximum amount of input and generated token history a model can consider at one time. Longer context can require more temporary memory.
- **KV cache:** Temporary stored attention information reused while generating a response, so the model does not need to recompute all previous-token information every time. It uses additional memory that grows with the conversation length.
- **Prompt:** The text or other input a person gives to a model, such as a question. `model_size.py` does not read or process prompts.
- **Token:** A piece of text, such as a word, part of a word, or punctuation, used by a language model. Prompt tokens are input data; they are not the model's learned parameters.
- **Tokenizer and token ID:** A tokenizer splits text into tokens and maps them to numeric IDs the model can process. This project’s model-size estimator does not tokenize text or count token IDs.
- **Embedding and activation:** Numeric representations and intermediate values created while a model processes input. Their memory is temporary working memory and is not included in the parameter-storage estimate.
- **Number format / precision:** The way each number is stored, including how many bits are used. `fp16` stores each number in 16 bits; lower precision generally uses less memory, though it can affect numerical accuracy.
- **Floating-point format:** A way to store numbers that may include a fractional part. `fp32`, `fp16`, and `bf16` are floating-point formats; `fp32` uses more memory per parameter than the 16-bit formats.
- **Integer format:** A way to store whole-number values. `int8` and `int4` use fewer bits than common floating-point formats and are often used after quantization.
- **Quantization:** Converting model weights into a lower-bit number format to reduce memory use and sometimes improve speed. It can slightly change a model's answers, and real quantized files may need extra scale information, so this project's simple estimate is approximate.
- **Memory estimate:** An approximate calculation of how much memory is needed to store model parameters. For parameter storage alone, 7 billion parameters at 16 bits each need about 14 billion bytes (roughly 14 GB in the project's simplified estimate). Real model use also needs memory for other data, so the estimate is not a guarantee that a model will run.
- **Bit and byte:** A bit is a single binary digit; a byte is eight bits. `model_size.py` multiplies the parameter count by the bits per parameter, then divides by eight to estimate bytes.
- **GB (gigabyte):** A decimal unit of memory equal to one billion bytes. The model size estimator reports decimal GB, so 14,000,000,000 bytes is 14 GB. Some computer tools use GiB (gibibytes), which is a different unit.
- **Floating-point and integer formats:** Ways to represent numbers. `fp32` uses 32 bits per parameter; `fp16` and `bf16` use 16; `int8` uses 8; and `int4` uses 4. The estimator assumes these values are stored densely, including two 4-bit values per byte for `int4`.
- **Parameter storage estimate:** The calculation in `estimate_memory_gb()` covers only the memory for model parameters. A running model also needs memory for temporary calculations, inputs, and other data, so actual memory use is higher.
- **Inference:** Using a trained model to produce an answer or prediction. Inference needs memory for weights and additional working data, so a model whose weights fit may still fail to run.
- **Activation and cache memory:** Temporary memory used while processing input and generating output. For a language model, longer conversations and larger batches can increase this memory; `model_size.py` does not estimate it.
- **Training memory:** Memory needed to adjust model weights during training. Training usually needs substantially more memory than merely storing weights because it also keeps gradients and optimizer data; this estimator does not estimate training requirements.
- **System RAM and VRAM:** RAM is the computer's main memory; VRAM is memory attached to a GPU. A model loaded on a GPU needs enough VRAM for its weights and working data. This estimate gives a size but does not inspect available RAM or VRAM or guarantee the model will fit.
- **Memory fit example:** If the estimate says 14 GB and a GPU has 8 GB of VRAM, the weights alone exceed that GPU memory. A GPU with 16 GB may still not have enough room for all working data.
- **Argument parser:** A tool that reads and checks values supplied after a terminal command. `argparse` lets `model_size.py` accept a parameter count and a precision, for example `python -m ailab.model_size 7000000000 fp16`.
- **Positional command-line argument:** A value supplied to a command in a specific order. In the model-size command, the first value is the parameter count and the second is the precision.
- **Input validation:** Checking that provided values are allowed before using them. The estimator rejects a nonpositive parameter count and unsupported precision names.
- **Dictionary:** A collection that maps keys to values. `BITS_PER_PARAMETER` maps names such as `fp16` to the number of bits used for each parameter.
- **Constant:** A value intended to stay fixed while a program runs. By convention, Python constant names are written in uppercase; `BITS_PER_PARAMETER` lists the supported storage formats.
- **`ValueError`:** A Python error used when a value has the right general type but is not acceptable. `estimate_memory_gb()` raises it for invalid parameter counts or unknown precision names.
- **`isinstance()`:** A built-in function that checks whether a value belongs to a given type. The estimator uses it to reject values such as a decimal or text where it expects an integer count.
- **Type checking:** Checking the kind of value supplied to a function. The model estimator checks for a whole-number parameter count before doing arithmetic.
- **Logical operator (`or`):** Combines conditions so the overall condition is true when either side is true. The parameter-count check rejects the input if it is a Boolean or is not an integer.
- **Boolean as an integer:** In Python, `bool` is technically a kind of `int`, so `True` behaves like `1`. The estimator explicitly rejects Booleans so `True` cannot accidentally mean one model parameter.
- **String normalization:** Converting text into a consistent form before comparing it. `precision.lower()` allows the function to accept `FP16` as well as `fp16`.
- **Dictionary membership and lookup:** `name in mapping` checks whether a key exists; `mapping[name]` retrieves its value. `BITS_PER_PARAMETER` is checked for the requested format, then used to retrieve its bit count.
- **`str.join()`:** Combines multiple strings with a chosen separator. `", ".join(BITS_PER_PARAMETER)` creates the readable list of supported formats for an error message.
- **`argparse` argument conversion and choices:** The command-line parser converts the first argument to an integer with `type=int`, lowercases the second with `type=str.lower`, and restricts it to known format names with `choices=...`.
- **Formatted number fields:** Formatting instructions control how numbers appear in output. `:.2f` shows two digits after the decimal point, while `:,` adds thousands separators to the parameter count.
- **Parser error:** A clear command-line error message that also shows usage information and ends the command with a failure exit code. `parser.error()` handles invalid values from the estimation function.

### Benchmark concepts

- **NumPy:** A Python library for working with arrays of numbers and performing mathematical operations. The benchmark uses NumPy arrays and its matrix multiplication operation.
- **NumPy backend and GPU limit:** This benchmark calls NumPy's `@` operation and does not call a GPU library such as CUDA. It measures the NumPy implementation available in the current Python environment, normally on the CPU; the `local` or `colab` label does not choose hardware.
- **Matrix multiplication operator (`@`):** Python syntax for multiplying matrices. In `benchmark.py`, `left @ right` multiplies the two NumPy input matrices and creates a result matrix.
- **Array:** An ordered group of values, often arranged in one or more dimensions. In the benchmark, each matrix is a two-dimensional NumPy array.
- **Matrix size:** The number of rows and columns in a square matrix. A size of 512 means each input has 512 rows and 512 columns.
- **Floating-point data type (`float32`):** A number format that uses 32 bits per value. The benchmark uses it for matrix elements to keep memory use and computation reasonable.
- **Random number generator:** A tool that produces number sequences for calculations. The benchmark uses NumPy's generator to create its input matrices.
- **Seed:** A starting value for a random number generator. Reusing the same seed makes it generate the same input matrices, helping make benchmark runs comparable.
- **NumPy random generator:** `np.random.default_rng(seed)` creates a generator used to make repeatable random matrices. Reusing the seed makes the same test inputs within compatible NumPy versions.
- **Repetition:** One measured run of the operation. The benchmark repeats matrix multiplication and records the average and fastest duration to reduce reliance on a single timing.
- **High-resolution timer:** A timer suited to measuring short durations accurately. `time.perf_counter()` measures how long each matrix multiplication takes.
- **Warm-up run:** An initial operation run before measurements begin. `benchmark.py` performs one multiplication first so one-time setup is less likely to distort the measured repetitions.
- **Platform information:** Details identifying the operating system and environment. The benchmark records `platform.platform()`, along with Python and NumPy versions, to give timing results context.
- **Path object:** A Python object representing a filesystem location. `Path("results") / filename` builds the output file location in a way that works across operating systems.
- **Parent directory:** The folder that contains a file. `output_path.parent.mkdir(parents=True, exist_ok=True)` creates missing output folders before writing the JSON file.
- **JSON serialization:** Converting Python data such as dictionaries, strings, numbers, and lists into JSON text. `json.dumps()` serializes the benchmark result before it is saved.
- **UTF-8:** A common text encoding that supports characters from many languages. `write_text(..., encoding="utf-8")` saves the JSON using UTF-8.
- **Timing scope:** The exact work included in a measurement. The benchmark times each NumPy `@` operation, including creation of its result array, but excludes creating the random input matrices and writing the JSON file.
- **JSON result file:** A saved record of benchmark settings and measurements. The CLI writes local results to `results/local_benchmark.json` or Colab results to `results/colab_benchmark.json` by default.
- **Benchmark environment label:** A name recorded with the results to say where the run happened, such as `local` or `colab`. The label is selected by the user; it does not itself detect or change the hardware.
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
