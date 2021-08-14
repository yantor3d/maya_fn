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


def elements(plug):
    """Yield the elements of the given array plug.

    Args:
        plug (str): Path to an array plug.

    Yields:
        str

    Raises:
        TypeError: If the given plug is not an array.
    """

    plug = _get_array_plug(plug)

    for i in plug.getExistingArrayAttributeIndices():
        yield plug.elementByLogicalIndex(i).name()


def indices(plug):
    """Yield the indices of the given array plug.

    Args:
        plug (str): Path to an array plug.

    Yields:
        int

    Raises:
        TypeError: If the given plug is not an array.
    """

    plug = _get_array_plug(plug)

    for i in plug.getExistingArrayAttributeIndices():
        yield i


def _get_array_plug(plug):
    """Return the given array plug."""

    plug = maya_fn.api.get_plug(plug)

    if not plug.isArray:
        raise TypeError("'{}' is not an array plug.".format(plug.name()))

    return plug


__functions__ = dict(
    __call__=staticmethod(make),
    **{
        obj.__name__: staticmethod(obj)
        for obj in locals().values()
        if inspect.isfunction(obj)
    }
)

plug = type("plug", (), __functions__)()
