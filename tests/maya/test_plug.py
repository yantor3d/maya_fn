"""Plug function set suite for plug functions."""

import pytest

from maya import cmds
from maya.api import OpenMaya

import maya_fn


@pytest.mark.parametrize(
    "args,expected",
    [
        (("node", "attr"), "node.attr"),
        (("node", "attr", "X"), "node.attrX"),
        (("node", "attr", 1), "node.attr[1]"),
        (("node", "attr", 1, 2), "node.attr[1][2]"),
        (("node", "parent", "child", 1, "attr", "X"), "node.parent.child[1].attrX"),
    ],
    ids=[
        "simple attribute",
        "triple attribute",
        "array attribute index",
        "matrix attribute indexes",
        "all of the above",
    ],
)
def test_get_plug(new_scene, args, expected):
    assert maya_fn.plug(*args) == expected


def test_get_plug_array():
    node = cmds.createNode("network")
    root = maya_fn.plug(node, "values")

    cmds.addAttr(node, longName="values", multi=True)
    cmds.setAttr(maya_fn.plug(root, 0), 1.0)
    cmds.setAttr(maya_fn.plug(root, 1), 1.0)
    cmds.setAttr(maya_fn.plug(root, 3), 1.0)

    expected = [0, 1, 3]
    actual = list(maya_fn.plug.indices(root))

    assert actual == expected, "plug_indices returned the wrong values"

    expected = ["network1.values[0]", "network1.values[1]", "network1.values[3]"]
    actual = list(maya_fn.plug.elements(root))

    assert actual == expected, "plug_elements returned the wrong values"


def test_get_plug_array_errors():
    node = cmds.createNode("network")
    root = maya_fn.plug(node, "values")

    cmds.addAttr(node, longName="values")

    with pytest.raises(TypeError):
        list(maya_fn.plug.indices(root))

    with pytest.raises(TypeError):
        list(maya_fn.plug.elements(root))


def test_get_connections():
    node = cmds.createNode("transform")
    node = cmds.createNode("transform", parent=node)
    node = cmds.createNode("transform", parent=node)

    node = maya_fn.dag.full_path(node)

    src = "|persp.visibility"
    dst = maya_fn.plug(node, "visibility")

    cmds.connectAttr(src, dst)

    expected = src
    actual = maya_fn.plug.source(dst)

    assert actual == expected, "plug_source returned the wrong values"

    expected = [dst]
    actual = maya_fn.plug.destinations(src)

    assert actual == expected, "plug_destinations returned the wrong values"
