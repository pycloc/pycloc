from os import PathLike
from typing import Dict, List, Set, Tuple, Union

AnyPath = Union[bytes, str, PathLike[str], PathLike[bytes]]
FlagValue = Union[None, bool, bytes, float, int, str, AnyPath, List[str], Set[str], Tuple[str, ...]]
Flags = Dict[str, FlagValue]
