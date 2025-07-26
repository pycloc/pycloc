from importlib.metadata import PackageNotFoundError, version

import pycloc.command as command
import pycloc.exceptions as exceptions
from pycloc.command import *  # noqa: F403
from pycloc.exceptions import *  # noqa: F403

__all__ = command.__all__ + exceptions.__all__

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    __version__ = "0.0.0"
