"""API function set test suite."""

import pytest

from maya.api import OpenMaya

import maya_fn


def test_get_dag_path():
    """Given a valid DAG object, the function returns a valid MDagPath."""

    dag = maya_fn.get_dag_path("persp")

    assert isinstance(dag, OpenMaya.MDagPath), "Wrong object type returned"
    assert dag.isValid(), "Invalid DAG path returned"
    assert OpenMaya.MFnDagNode(dag).name() == "persp", "Wrong object returned"


def test_get_dag_path_errors_on_dg_node():
    """Given a valid, DG object, the function raises a TypeError."""

    with pytest.raises(ValueError):
        maya_fn.get_dag_path("time1")


def test_get_depend_node():
    node = maya_fn.get_object("time1")

    assert node is not None
    assert not node.isNull()


def test_get_depend_node_with_object_that_does_not_exist():
    with pytest.raises(LookupError):
        maya_fn.get_object("foobar")


@pytest.mark.parametrize("value", [None, 123], ids=["Null", "Integer"])
def test_get_depend_node_with_invalid_type(value):
    with pytest.raises(ValueError):
        maya_fn.get_object(value)


def test_get_plug():
    """Given a valid plug, the function returns a valid MPlug."""

    plug = maya_fn.get_plug("persp.message")

    assert isinstance(plug, OpenMaya.MPlug), "Wrong object type returned"
    assert not plug.isNull, "Null MPlug returned"
    assert plug.name() == "persp.message", "Wrong object returned"


def test_get_plug_errors():
    """Given an invalid plug, the function raises an error."""

    with pytest.raises(LookupError):
        maya_fn.get_plug("persp.foobar")

    with pytest.raises(TypeError):
        maya_fn.get_plug("persp")