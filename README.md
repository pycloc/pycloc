# pycloc

[![PyPI](https://img.shields.io/pypi/v/pycloc)](https://pypi.org/project/pycloc/)

<p align="center">
    <img src="https://pycloc.github.io/pycloc/assets/images/pycloc.png" alt="pycloc logo" />
</p>

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
