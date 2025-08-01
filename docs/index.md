# pycloc

Python wrapper for the [`cloc`](https://github.com/AlDanial/cloc) (Count Lines of Code) command-line tool.
This library provides a convenient, Pythonic interface to the powerful static analysis tool,
enabling you to count lines of code directly from your Python applications with comprehensive
error handling and dynamic configuration.

> [!WARNING]
> This library is currently in **Alpha**.
> APIs and core features may change without notice based on community feedback and requests.
> Documentation may be incomplete or outdated, and you should expect bugs and missing functionalities.

## Key Features

- **Platform Agnostic**: Can run on any operating system out: macOS, Linux and Windows;
- **Zero Dependencies**: No third-party Python dependencies, only requiring the Perl interpreter;
- **Dynamic Configuration**: Set CLI tool flags as Python attributes with automatic conversion;
- **Comprehensive Error Handling**: Custom exception hierarchy for different error scenarios;
- **Type Safety**: Full type annotations for better IDE support and code quality.

## Requirements

- **Python**: 3.10+
- **Perl**: 5.6.1+ (required for `cloc` execution)

> [!NOTE]
> Since `cloc` is written in Perl,
> you must ensure that the interpreter is installed and available in your system's `PATH`.
> This should work out of the box on most Unix-like systems,
> but may require additional setup on minimalistic Linux distros or Windows.

## Installation

To include the package in your project, run the following:

=== "pip"

    ```sh
    pip install pycloc
    ```

=== "pdm"

    ```sh
    pdm add pycloc
    ```

=== "poetry"

    ```sh
    poetry add pycloc
    ```

=== "uv"

    ```sh
    uv add pycloc
    ```

## Quick Start

```py linenums="1" title="example.py"
import json
from pathlib import Path

from pycloc import CLOC

target = Path("directory", "of", "your", "choice")

cloc = CLOC(
    workdir=target,
    timeout=30,  # (1)!
    json=True,  # (2)!
)

cloc.max_file_size = 5  # (3)!
output = cloc(  # (5)!
    ".", by_file=True,  # (4)!
)
result = json.loads(output)
pretty = json.dumps(obj=result, indent=4)

print(pretty)
```

1. Configurations can be supplied within the command constructor.
   Types such as `int`, `byte` or `Path` are stringified.
   This example is equivalent to passing `--timeout=30` in CLI.
2. Flags of type `bool` are serialized as on/off flags: `flag_name=True`
   is serialized as `--flag-name`, while `False` values are omitted entirely.
3. Configurations can also be specified through attribute setters.
   Note that specifying configurations this way **will** modify the instance.
4. Finally, you can pass additional configurations prior to execution.
   Note that configurations applied this way **do not** modify the instance.
5. Invokes the pre-configured command! (this can be done any number of times)
