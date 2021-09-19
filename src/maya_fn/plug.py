"""Maya Plug functions."""

import inspect
import six

from maya import cmds
from maya.api import OpenMaya

import maya_fn.api

__all__ = [
    "plug",
]


def attr(plug):
    """Return the attribute of the given plug.

    Args:
        plug (str): Path to an plug.

    Returns:
        str
    """

    plug = maya_fn.api.get_plug(plug)

    return plug.partialName(
        includeNonMandatoryIndices=True,
        includeInstancedIndices=True,
        useFullAttributePath=True,
        useLongNames=True,
    )


def destinations(plug):
    """Return the outputs of the given plug.

    Args:
        plug (str): Path to an plug.

    Returns:
        list[str]
    """

    plug = maya_fn.api.get_plug(plug)

    plugs = plug.connectedTo(False, True)

    return cmds.ls([p.name() for p in plugs], long=True)


def downstream(plug):
    """Return the nodes downstream the given plug.

    Args:
        plug (str): Path to an plug.

    Returns:
        list[str]
    """

    return [node(each) for each in destinations(plug)]


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


get = maya_fn.api.get_plug


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


def node(plug):
    """Return the node of the given plug.

    Args:
        plug (str): Path to an plug.

    Returns:
        str
    """

    plug = maya_fn.api.get_plug(plug)
    obj = plug.node()

    if obj.hasFn(OpenMaya.MFn.kDagNode):
        return OpenMaya.MFnDagNode(obj).fullPathName()
    else:
        return OpenMaya.MFnDependencyNode(obj).name()


def source(plug):
    """Return the source of the given plug.

    Args:
        plug (str): Path to an plug.

    Returns:
        str | None
    """

    plug = maya_fn.api.get_plug(plug)

    plugs = plug.connectedTo(True, False)
    plugs = [make(node(p), attr(p)) for p in plugs]

    if plugs:
        return plugs[0]
    else:
        return None


def split(plug):
    """Return the node and attribute of the given plug."""

    return node(plug), attr(plug)


def upstream(plug):
    """Return the node upstream the given plug.

    Args:
        plug (str): Path to an plug.

    Returns:
        list[str]
    """

    p = source(plug)

    return p if p is None else source(p)


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
