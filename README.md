# pycloc

Python wrapper for the [cloc](https://github.com/AlDanial/cloc) CLI tool.
This package is currently available on PyPI as `pycloctest` and installable via `pip install pycloctest`.
We are working to move it to `pycloc` on PyPI.

## Requirements

To use the library in your codebase, you will need Python 3.10 or newer.

> [!NOTE]
> Since this script is written in Perl, you must make sure that its interpreter is installed and located on your `PATH`.
> Should work out of the box on most systems (as the majority of Unix-like systems have it installed by default),
> but worth pointing out in case you plan on using this on a minimalistic Linux image or Windows.

For local development, you will also need:

- [`uv`](https://github.com/astral-sh/uv) package manager;
- [`just`](https://github.com/casey/just) command runner;

## Example

```python
import json
from pathlib import Path

from pycloc import CLOC

cwd = Path.cwd()
cloc = CLOC(
    workdir=cwd,
    timeout=30,
    by_file=True,
    json=True,
    exclude_dir=(
        ".idea",
        ".venv",
    ),
)

output = cloc(".")
result = json.loads(output)
pretty = json.dumps(
    obj=result,
    indent=4,
)

print(pretty)
```

## FAQ

### How can I request a feature or ask a question?

If you have ideas for a feature that you would like to see implemented or if you have any questions, we encourage you to
create a new [discussion](https://github.com/USIREVEAL/pycloc/discussions).
By initiating a discussion, you can engage with the community and our team,
and we will respond promptly to address your queries or consider your feature requests.

### How can I report a bug?

To report any issues or bugs you encounter, create a [new issue](https://github.com/USIREVEAL/pycloc/issues).
Providing detailed information about the problem you're facing will help us understand and address it more effectively.
Rest assured, we're committed to promptly reviewing and responding to the issues you raise,
working collaboratively to resolve any bugs and improve the overall user experience.
