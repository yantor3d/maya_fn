"""DAG function set test suite."""

import pytest

from maya import cmds

import maya_fn


def test_get_ancestores():
    """Given a valid DAG object, the function returns all parent transforms."""

    x = cmds.createNode("transform", name="x")
    a = cmds.createNode("transform", name="a", parent=x)
    b = cmds.createNode("transform", name="b", parent=a)
    c = cmds.createNode("transform", name="c", parent=b)

    expected = sorted(cmds.ls([x, a, b], long=True), key=lambda n: n.count("|"))
    actual = maya_fn.dag.ancestors(c)

    assert actual == expected

    assert maya_fn.dag.ancestors(x) == []


def test_get_children():
    """Given a valid DAG object, the function returns the full path of its children."""

    root = cmds.createNode("transform")

    cmds.createNode("locator", parent=root)
    cmds.createNode("transform", parent=root)
    cmds.createNode("transform", parent=root)

    expected = cmds.listRelatives(root, children=True, type="transform", fullPath=True)
    actual = maya_fn.dag.children(root)

    assert set(actual) == set(expected), "get_children returned the wrong results"


def test_get_descendents():
    """Given a valid DAG object, the function returns the full path of its descendents."""

    cmds.file(new=True, force=True)

    x = cmds.createNode("transform", name="x")
    a = cmds.createNode("transform", name="a", parent=x)
    b = cmds.createNode("transform", name="b", parent=a)
    c = cmds.createNode("transform", name="c", parent=b)

    expected = sorted(cmds.ls([a, b, c], long=True), key=lambda n: n.count("|"))
    actual = list(maya_fn.dag.descendents(x))

    assert actual == expected, "descendents returned the wrong results"


def test_get_full_path():
    """Given a valid DAG object, the function returns the its full name."""

    root = cmds.createNode("transform")
    child = cmds.createNode("transform", parent=root)
    child = cmds.createNode("transform", parent=child)
    child = cmds.createNode("transform", parent=child)

    expected = cmds.ls(child, long=True)[0]
    actual = maya_fn.dag.full_path(child)

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
    actual = maya_fn.dag.name(child)

    assert actual == expected, "get_name returned the wrong results"


def test_get_parent():
    """Given a valid DAG object, the function returns the full path of its shapes."""

    root = cmds.createNode("transform")
    child = cmds.createNode("transform", parent=root)
    shape = cmds.createNode("locator", parent=child)

    assert maya_fn.dag.parent(root) is None
    assert maya_fn.dag.parent(child) == maya_fn.dag.path(root).fullPathName()
    assert maya_fn.dag.parent(shape) == maya_fn.dag.path(child).fullPathName()


def test_get_shapes():
    """Given a valid, DG object, the function raises a TypeError."""

    root = cmds.createNode("transform")

    cmds.createNode("locator", parent=root)
    cmds.createNode("transform", parent=root)
    cmds.createNode("transform", parent=root)

    expected = cmds.listRelatives(root, children=True, type="shape", fullPath=True)
    actual = maya_fn.dag.shapes(root)

    assert set(actual) == set(expected), "get_children returned the wrong results"


def test_get_siblings():
    """Given a valid DAG object, the function returns all sibling DAG nodes."""

    cmds.file(new=True, force=True)

    root = cmds.createNode("transform", name="root")
    x = cmds.createNode("transform", name="x", parent=root)
    a = cmds.createNode("transform", name="a", parent=x)
    b = cmds.createNode("transform", name="b", parent=x)
    c = cmds.createNode("transform", name="c", parent=x)
    y = cmds.createNode("transform", name="y", parent=root)
    z = cmds.createNode("transform", name="z", parent=y)

    expected = set(cmds.ls([b, c], long=True))
    actual = set(maya_fn.dag.siblings(a))

    assert actual == expected
    assert maya_fn.dag.siblings(z) == []

    assert set(maya_fn.dag.siblings(root)) == {"|persp", "|top", "|front", "|side"}
