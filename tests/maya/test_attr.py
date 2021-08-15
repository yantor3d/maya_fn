"""Attribute function set test suite."""

import pytest

from maya import cmds

import maya_fn


def test_add_attr():
    node = cmds.createNode("transform", parent=cmds.createNode("transform"))
    node = maya_fn.dag.full_path(node)

    expected = maya_fn.plug(node, "foobar")
    actual = maya_fn.attr.add(node, ln="foobar")

    assert expected == actual


def test_add_compound_attr():
    node = cmds.createNode("transform")
    node = maya_fn.dag.full_path(node)

    expected = maya_fn.plug(node, "fizz", "buzz")

    maya_fn.attr.add(node, ln="fizz", at="compound", nc=1)
    actual = maya_fn.attr.add(node, ln="buzz", p="fizz")

    assert expected == actual
