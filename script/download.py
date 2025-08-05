#!/usr/bin/env -S uv run --active --script --quiet
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "from-root",
#   "requests",
#   "tqdm",
# ]
# ///
import json
from configparser import ConfigParser
from hashlib import sha256
from os import chmod
from os import environ as env
from sys import stdout
from textwrap import dedent
from typing import Dict, Optional

import requests
from from_root import from_root
from tqdm import tqdm

resources = from_root("src", "pycloc", "resources", mkdirs=True)


def token() -> Optional[str]:
    return f"Bearer {value}" if (value := env.get("GITHUB_TOKEN")) else None


def headers() -> Dict[str, str]:
    return {
        "Accept": "application/vnd.github+json",
        "Authorization": token(),
        "User-Agent": "pycloc-downloader",
    }


def progressbar(
    desc: str,
    total: Optional[int] = None,
):
    return tqdm(
        file=stdout,
        total=total,
        desc=desc,
        bar_format="{desc}: {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]",
        unit="iB",
        unit_scale=True,
        unit_divisor=1024,
    )


def main():
    response = requests.get(
        url="https://api.github.com/repos/AlDanial/cloc/releases/latest",
        headers=headers(),
        stream=True,
    )

    length = int(response.headers.get("content-length", 0))
    buffer = bytes()

    with progressbar(
        total=length,
        desc="Getting Latest Release",
    ) as bar:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                buffer += chunk
                bar.update(len(chunk))

    release = json.loads(buffer)
    assets = release.get("assets", [])
    asset, *_ = [asset for asset in assets if asset.get("content_type") == "application/x-perl"]

    response = requests.get(
        url=asset.get("browser_download_url"),
        headers=headers(),
        stream=True,
    )

    digest = sha256()
    length = int(response.headers.get("content-length", 0))

    script = resources / "cloc.pl"
    with (
        progressbar(
            total=length,
            desc="Downloading Perl Script",
        ) as bar,
        open(
            file=script,
            mode="wb",
        ) as buffer,
    ):
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                buffer.write(chunk)
                digest.update(chunk)
                bar.update(len(chunk))

    *_, expected = asset.get("digest").split(sep=":", maxsplit=1)
    actual = digest.hexdigest()
    assert expected == actual, dedent(f"""
    Checksum missmatch!
    Expected: {expected}
    Actual:   {actual}
    """).strip()
    chmod(path=script, mode=0o755)

    config = ConfigParser(default_section="cloc")
    config.set(
        section="cloc",
        option="url",
        value="https://github.com/AlDanial/cloc",
    )
    config.set(
        section="cloc",
        option="version",
        value=release.get("name"),
    )
    config.set(
        section="cloc",
        option="sha256",
        value=actual,
    )
    with open(
        file=resources / "cloc.ini",
        mode="w",
    ) as buffer:
        config.write(buffer)


if __name__ == "__main__":
    main()
