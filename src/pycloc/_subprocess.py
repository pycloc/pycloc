from asyncio import create_subprocess_exec as create_async_subprocess
from logging import Logger
from logging import getLogger as get_logger
from shutil import which
from subprocess import PIPE, CalledProcessError
from subprocess import run as create_subprocess
from typing import Iterable, Literal, Optional, Sequence, Tuple, overload

from pycloc._aliases import AnyPath, CommandOutput, Flag
from pycloc._serialization import serialize

empty: Tuple[str, ...] = ()

logger: Logger = get_logger(__package__)


def perl() -> Optional[AnyPath]:
    return which(cmd="perl")


async def run_async(
    args: Sequence[AnyPath],
    cwd: Optional[AnyPath] = None,
    encoding: Optional[str] = None,
    errors: Optional[str] = None,
) -> str:
    process = await create_async_subprocess(
        *args,
        cwd=cwd,
        stdout=PIPE,
        stderr=PIPE,
    )

    stdout, stderr = await process.communicate()

    if process.returncode:
        raise CalledProcessError(
            returncode=process.returncode,
            cmd=args,
            output=stdout,
            stderr=stderr,
        )

    if stderr := stderr.strip():
        for line in stderr.splitlines():
            decoded = line.decode(
                encoding=encoding or "utf-8",
                errors=errors or "strict",
            )
            logger.warning(decoded)

    return stdout.decode(
        encoding=encoding or "utf-8",
        errors=errors or "strict",
    )


def run_sync(
    args: Sequence[AnyPath],
    cwd: Optional[AnyPath] = None,
    encoding: Optional[str] = None,
    errors: Optional[str] = None,
) -> str:
    process = create_subprocess(
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


@overload
def run(
    executable: AnyPath,
    arguments: Iterable[AnyPath] = empty,
    flags: Iterable[Flag] = empty,
    cwd: Optional[AnyPath] = None,
    encoding: Optional[str] = None,
    errors: Optional[str] = None,
    asynchronous: Literal[False] = False,
) -> str: ...


@overload
async def run(
    executable: AnyPath,
    arguments: Iterable[AnyPath] = empty,
    flags: Iterable[Flag] = empty,
    cwd: Optional[AnyPath] = None,
    encoding: Optional[str] = None,
    errors: Optional[str] = None,
    asynchronous: Literal[True] = True,
) -> str: ...


def run(
    executable: AnyPath,
    arguments: Iterable[AnyPath] = empty,
    flags: Iterable[Flag] = empty,
    cwd: Optional[AnyPath] = None,
    encoding: Optional[str] = None,
    errors: Optional[str] = None,
    asynchronous: bool = False,
) -> CommandOutput:
    args = [executable, *arguments] + [
        serialized
        for name, value in flags
        if value is not None
        for serialized in serialize(
            name=name,
            value=value,
            encoding=encoding,
            errors=errors,
        )
    ]

    cmd = " ".join(str(arg) for arg in args)
    logger.debug("cmd: %s", cmd)
    logger.debug("cwd: %s", cwd)
    return (
        run_async(
            args=args,
            cwd=cwd,
            encoding=encoding,
            errors=errors,
        )
        if asynchronous
        else run_sync(
            args=args,
            cwd=cwd,
            encoding=encoding,
            errors=errors,
        )
    )
