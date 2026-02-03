# pycloc

<p align="center">
    <img src="https://pycloc.github.io/pycloc/assets/images/pycloc.png" alt="pycloc logo" />
</p>

<p align="center">
    <a href="https://github.com/pycloc/pycloc/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/github/license/pycloc/pycloc.svg?color=blue"></a>
    <a href="https://pycloc.github.io/pycloc/"><img alt="Documentation" src="https://img.shields.io/website?label=documentation&url=https%3A%2F%2Fpycloc.github.io%2Fpycloc&down_color=red&down_message=offline&up_color=green&up_message=online"></a>
    <a href="https://github.com/pycloc/pycloc/releases"><img alt="GitHub release" src="https://img.shields.io/github/release/pycloc/pycloc.svg"></a>
    <a href="https://pypi.org/project/pycloc/"><img alt="PyPI" src="https://img.shields.io/badge/pypi-pycloc-green"></a>
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

## License

The Python source code in this project is licensed under the MIT License.

> [!IMPORTANT]
> This project bundles the `cloc` command-line program, which is a separate
> work licensed under the GNU General Public License version 2.0 (GPL-2.0). 
> `cloc` is not part of this project’s source code and remains licensed under GPL-2.0. See [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md) and [LICENSE-GPL-2.0](LICENSE-GPL-2.0) for details.