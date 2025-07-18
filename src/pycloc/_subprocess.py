import subprocess
from logging import Logger
from logging import getLogger as get_logger
from shutil import which
from typing import Iterable, Optional, Tuple

from pycloc._aliases import AnyPath

empty: Tuple[str, ...] = ()

logger: Logger = get_logger(__package__)


def perl() -> Optional[AnyPath]:
    return which(cmd="perl")


def run(
    executable: AnyPath,
    arguments: Iterable[AnyPath] = empty,
    flags: Iterable[str] = empty,
    cwd: Optional[AnyPath] = None,
    encoding: Optional[str] = None,
    errors: Optional[str] = None,
) -> str:
    args = [executable, *arguments, *flags]
    cmd = " ".join(str(arg) for arg in args)
    logger.debug("cmd: %s", cmd)
    logger.debug("cwd: %s", cwd)

    process = subprocess.run(
        args=args,
        cwd=cwd,
        encoding=encoding,
        errors=errors,
        capture_output=True,
        check=True,
        text=True,
    )

    if stderr := process.stderr.strip():
        for line in stderr.splitlines():
            logger.warning(line)

    return process.stdout
