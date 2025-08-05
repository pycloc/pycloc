#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "from-root",
#   "questionary",
# ]
# ///
from os import execlp
from shutil import which

import questionary
from from_root import from_root

examples = from_root("examples").absolute()

uv = which("uv")


def main():
    question = questionary.select(
        message="Which example would you like to run?",
        choices=("sync", "async"),
    )
    example = question.ask() + ".py"
    # https://stackoverflow.com/a/6743663/17173324
    execlp(uv, uv, "run", examples / example)


if __name__ == "__main__":
    main()
