# pycloc

Python wrapper for the [cloc](https://github.com/AlDanial/cloc) CLI tool. This package currently available on PyPI as `pycloctest` and installable via `pip install pycloctest`.
We are working to move it to `pycloc` on PyPI.

## Requirements

This library requires you to have `cloc` installed on your system.

> [!NOTE]  
> Since this script is written in Perl, you must make sure that its interpreter is installed and located on your `PATH`.
> Should work out of the box on most systems (as the majority of Unix-like systems have it installed by default),
> but worth pointing out in case you plan on using this on a minimalistic Linux image or Windows.

## Example

```python
from pycloc import CLOC
import json

if __name__ == "__main__":
    result = json.loads(CLOC().add_flag("--by-file")
                    .add_flag("--json")
                    .add_option("--timeout", 30)
                    .set_working_directory('./')
                    .add_argument('b95e1a662d44ad70dda1744baf6cd91606fc6702')
                    .execute())

    print(json.dumps(result, indent=4))
```

## Options

The API currently maps only a subset of the `cloc` command-line options. Support for other flags and parameters will be added as development progresses. All arbitrary flags can be passed using the `add_flag` method.

## FAQ

### How can I request a feature or ask a question?

If you have ideas for a feature that you would like to see implemented or if you have any questions, we encourage you to
create a new [discussion](https://github.comUSIREVEAL/pycloc/discussions). By initiating a discussion, you can engage with the community and our
team, and we will respond promptly to address your queries or consider your feature requests.

### How can I report a bug?

To report any issues or bugs you encounter, create a [new issue](https://github.com/USIREVEAL/pycloc/issues). Providing detailed information about
the problem you're facing will help us understand and address it more effectively. Rest assured, we're committed to
promptly reviewing and responding to the issues you raise, working collaboratively to resolve any bugs and improve the
overall user experience.
