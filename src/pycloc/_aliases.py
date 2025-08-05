from os import PathLike
from typing import Awaitable, Dict, List, Set, Tuple, Union

AnyPath = Union[bytes, str, PathLike[str], PathLike[bytes]]
CommandOutput = Union[str, Awaitable[str]]
FlagValue = Union[None, bool, bytearray, bytes, float, int, str, AnyPath, List[str], Set[str], Tuple[str, ...]]
Flags = Dict[str, FlagValue]
Flag = Tuple[str, FlagValue]
