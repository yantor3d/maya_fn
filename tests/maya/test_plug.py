"""Plug function set test suite."""

import pytest

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
