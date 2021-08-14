"""DAG function set test suite."""

import pytest

from maya import cmds

import maya_fn


def test_get_children():
    """Given a valid DAG object, the function returns the full path of its children."""

    root = cmds.createNode("transform")

    cmds.createNode("locator", parent=root)
    cmds.createNode("transform", parent=root)
    cmds.createNode("transform", parent=root)

    expected = cmds.listRelatives(root, children=True, type="transform", fullPath=True)
    actual = maya_fn.get_children(root)

    assert set(actual) == set(expected), "get_children returned the wrong results"


def test_get_full_path():
    """Given a valid DAG object, the function returns the its full name."""

    root = cmds.createNode("transform")
    child = cmds.createNode("transform", parent=root)
    child = cmds.createNode("transform", parent=child)
    child = cmds.createNode("transform", parent=child)

    expected = cmds.ls(child, long=True)[0]
    actual = maya_fn.get_full_path(child)

    assert actual == expected, "get_full_path returned the wrong results"


def test_get_name():
    """Given a valid DAG object, the function returns the its short name."""

    root = cmds.createNode("transform")
    child = cmds.createNode("transform", parent=root)
    child = cmds.createNode("transform", parent=child)
    child = cmds.createNode("transform", name="foobar", parent=child)
    (child,) = cmds.ls(child, long=True)

    cmds.duplicate(root)

    expected = "foobar"
    actual = maya_fn.get_name(child)

    assert actual == expected, "get_name returned the wrong results"


def test_get_parent():
    """Given a valid DAG object, the function returns the full path of its shapes."""

    root = cmds.createNode("transform")
    child = cmds.createNode("transform", parent=root)
    shape = cmds.createNode("locator", parent=child)

    assert maya_fn.get_parent(root) is None
    assert maya_fn.get_parent(child) == maya_fn.get_dag_path(root).fullPathName()
    assert maya_fn.get_parent(shape) == maya_fn.get_dag_path(child).fullPathName()


def test_get_shapes():
    """Given a valid, DG object, the function raises a TypeError."""

    root = cmds.createNode("transform")

    cmds.createNode("locator", parent=root)
    cmds.createNode("transform", parent=root)
    cmds.createNode("transform", parent=root)

    expected = cmds.listRelatives(root, children=True, type="shape", fullPath=True)
    actual = maya_fn.get_shapes(root)

    assert set(actual) == set(expected), "get_children returned the wrong results"
