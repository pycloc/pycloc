#!/usr/bin/env -S uv run --active --script --quiet
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "from-root",
# ]
# ///
from shutil import rmtree

from from_root import from_root

resources = from_root("src", "pycloc", "resources")
for name in ("cloc.pl", "cloc.ini"):
    resource = resources / name
    resource.unlink(missing_ok=True)

for name in (".coverage", "coverage.md"):
    file = from_root(name)
    file.unlink(missing_ok=True)

for name in ("dist", "htmlcov", "site"):
    directory = from_root(name)
    rmtree(directory, ignore_errors=True)
