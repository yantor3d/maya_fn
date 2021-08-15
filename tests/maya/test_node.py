"""Attribute function set test suite."""

import pytest

from maya import cmds

import maya_fn


def test_add_attr():
    node = cmds.createNode("transform", parent=cmds.createNode("transform"))
    node = maya_fn.dag.full_path(node)

    expected = maya_fn.plug(node, "foobar")
    actual = maya_fn.node.add_attr(node, ln="foobar")

    assert expected == actual

    with pytest.raises(ValueError):
        maya_fn.node.add_attr(node)

    expected = ["|persp.foobar", "|front.foobar", "|top.foobar", "|side.foobar"]
    actual = maya_fn.node.add_attr("persp", "front", "top", "side", ln="foobar")

    assert expected == actual


def test_add_compound_attr():
    node = cmds.createNode("transform")
    node = maya_fn.dag.full_path(node)

    expected = maya_fn.plug(node, "fizz", "buzz")

    maya_fn.node.add_attr(node, ln="fizz", at="compound", nc=1)
    actual = maya_fn.node.add_attr(node, ln="buzz", p="fizz")

    assert expected == actual
