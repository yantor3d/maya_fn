"""Maya Plug functions."""

import inspect
import six

import maya_fn.api

__all__ = [
    "plug",
]


def make(*args):
    """Return the plug built up from the given arguments.

    Args:
        *args (str | int): Token(s) to build the plug name from.

    Returns:
        str
    """

    parts = []

    for arg in args:
        if isinstance(arg, int):
            parts[-1] = "{}[{}]".format(parts[-1], arg)
        elif isinstance(arg, six.string_types) and len(arg) == 1:
            parts[-1] = "{}{}".format(parts[-1], arg)
        else:
            parts.append(arg)

    return ".".join(parts)


make.__alias__ = "__call__"


def elements(array_plug):
    """Yield the elements of the given array plug.

    Args:
        array_plug (str): Path to an array plug.

    Yields:
        str

    Raises:
        TypeError: If the given plug is not an array.
    """

    _plug = maya_fn.api.get_plug(array_plug)

    if not _plug.isArray:
        raise TypeError("'{}' is not an array plug.".format(_plug.name()))

    for i in _plug.getExistingArrayAttributeIndices():
        yield _plug.elementByLogicalIndex(i).name()


def indices(array_plug):
    """Yield the indices of the given array plug.

    Args:
        array_plug (str): Path to an array plug.

    Yields:
        int

    Raises:
        TypeError: If the given plug is not an array.
    """

    _plug = maya_fn.api.get_plug(array_plug)

    if not _plug.isArray:
        raise TypeError("'{}' is not an array plug.".format(_plug.name()))

    for i in _plug.getExistingArrayAttributeIndices():
        yield i


__functions__ = {
    getattr(obj, "__alias__", obj.__name__): staticmethod(obj)
    for obj in locals().values()
    if inspect.isfunction(obj)
}

plug = type("plug", (), __functions__)()
