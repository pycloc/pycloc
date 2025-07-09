import subprocess
from logging import Logger
from logging import getLogger as get_logger
from typing import Iterable, Optional, Tuple

from pycloc._aliases import AnyPath

empty: Tuple[str, ...] = ()

logger: Logger = get_logger(__package__)


def run(
    executable: AnyPath,
    arguments: Iterable[AnyPath] = empty,
    flags: Iterable[str] = empty,
    cwd: Optional[AnyPath] = None,
) -> str:
    args = [executable, *arguments, *flags]
    logger.debug("cmd: %s", " ".join(args))
    logger.debug("cwd: %s", cwd)

    process = subprocess.run(
        args=args,
        cwd=cwd,
        capture_output=True,
        check=True,
        text=True,
    )

    if stderr := process.stderr.strip():
        for line in stderr.splitlines():
            logger.warning(line)

    return process.stdout
