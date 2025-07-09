from typing import Any


def is_property(instance: Any, name: str) -> bool:
    cls = type(instance)
    if not hasattr(cls, name):
        return False
    attr = getattr(cls, name, None)
    return isinstance(attr, property)
