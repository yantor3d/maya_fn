"""Dependency node utilities."""

import six

from maya import cmds
from maya.api import OpenMaya

import maya_fn.plug

__all__ = [
    "create",
]


def create(node_type, name=None, **kwargs):
    """Create a new node in the graph, with connections/values.
    
    Args:
        node_type (str): Type of node to create.
        name (str): Optional name for the new node.
        kwargs (dict[str, Any]): Map of attribute name -> value to set/connect

    Returns:
        str
    """

    name = name or '{}#'.format(node_type)
    node = cmds.createNode(node_type, name=name, skipSelect=True)

    for attr, value in kwargs.items():
        if cmds.attributeQuery(attr, node=node, writable=True):
            _set_or_connect_attr(node, attr, value)
        else:
            _connect_attr(node, attr, value)

    return node


def _connect_attr(node, attr, value):
    """Connect the given output attribute.
    
    Args:
        node (str): Name of a DG node.
        attr (str): Attribute to connect.
        value (Any): Destination plug(s).
    """

    if not cmds.attributeQuery(attr, node=node, exists=True):
        return

    plug = maya_fn.plug(node, attr)

    if isinstance(value, dict):
        for k, v in value.items():
            _connect_attr(node, maya_fn.plug(attr, k), v)
    elif isinstance(value, (list, tuple)):
        num_attrs, = cmds.attributeQuery(attr, node=node, numberOfChildren=True) or [0]
        num_items = len(value)

        if num_items == num_attrs:
            children = cmds.attributeQuery(attr, node=node, listChildren=True)

            for child, val in zip(children, value):
                _connect_attr(node, child, val)
            return
        
        if cmds.attributeQuery(attr, node=node, multi=True):
            for i, v in enumerate(value):
                _connect_attr(node, maya_fn.plug(attr, i), v)
            return

        for v in value:
            _connect_attr(node, attr, v)
    elif isinstance(value, six.string_types):
        if cmds.objExists(value):
            cmds.connectAttr(plug, value)
        else:
            raise RuntimeError((node, attr, value))
    else:
        raise RuntimeError((node, attr, value))


def _set_or_connect_attr(node, attr, value):
    """Set or connect the given input attribute.
    
    Args:
        node (str): Name of a DG node.
        attr (str): Attribute to set or connect.
        value (Any): Source plug(s) or value(s)
    """

    if not cmds.attributeQuery(attr, node=node, exists=True):
        return

    plug = maya_fn.plug(node, attr)

    if isinstance(value, dict):
        for k, v in value.items():
            _set_or_connect_attr(node, maya_fn.plug(attr, k), v)
    elif isinstance(value, (list, tuple)):
        if (
            cmds.getAttr(plug, type=True) == 'matrix'
            and len(value) == 16
        ):
            cmds.setAttr(plug, value, type='matrix')
            return

        num_items = len(value)
        num_attrs, = cmds.attributeQuery(attr, node=node, numberOfChildren=True) or [0]

        if num_items == num_attrs:
            children = cmds.attributeQuery(attr, node=node, listChildren=True)

            for child, val in zip(children, value):
                _set_or_connect_attr(node, child, val)
            return 
        
        if cmds.attributeQuery(attr, node=node, multi=True):
            for i, v in enumerate(value):
                _set_or_connect_attr(node, maya_fn.plug(attr, i), v)
            return

        raise RuntimeError((node, attr, value))
    elif isinstance(value, six.string_types):
        if cmds.objExists(value):
            cmds.connectAttr(value, plug)
        elif cmds.getAttr(plug, type=True) == 'string':
            cmds.setAttr(plug, value, type='string')
        else:
            raise RuntimeError((node, attr, value))
    else:
        cmds.setAttr(plug, value)
