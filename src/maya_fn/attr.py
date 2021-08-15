"""Maya attribute function set."""

from maya import cmds

import maya_fn.plug

__all__ = [
    "add",
]


def add(*args, **kwargs):
    """Add an attribute to the node(s) and return the new plug(s).

    Returns:
        str | list[str]
    """

    attr_name = kwargs.get("longName") or kwargs.get("ln")
    parent = kwargs.get("parent") or kwargs.get("p")

    if not attr_name:
        raise ValueError("An attribute name was not specified.")

    cmds.addAttr(*args, **kwargs)

    values = [parent, attr_name] if parent else [attr_name]

    nodes = cmds.ls(args, long=True)
    plugs = [maya_fn.plug(node, *values) for node in nodes]

    if len(plugs) == 1:
        return plugs[0]
    else:
        return plugs
