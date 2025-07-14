from configparser import ConfigParser
from dataclasses import dataclass

from pycloc._resources import metadata

default: str = "???"
section: str = "cloc"

config: ConfigParser = ConfigParser(default_section=section)

config.read(filenames=metadata())


@dataclass
class CLOCProperties:
    sha256: str = default
    url: str = default
    version: str = default


properties: CLOCProperties = CLOCProperties(**config.defaults())
