"""DAG node utilities."""

from maya.api import OpenMaya

import maya_fn.api

__all__ = [
    "get_children",
    "get_full_path",
    "get_name",
    "get_parent",
    "get_shapes",
]


def get_children(dag_node):
    """Return the children transforms of the given node.

    Args:
        dag_node (str): DAG node in the current scene.

    Returns:
        list[str]
    """

    return [
        child.fullPathName()
        for child in _iter_children(dag_node)
        if child.node().hasFn(OpenMaya.MFn.kTransform)
    ]


def get_full_path(dag_node):
    """Return the full path of the given dag node.

    Args:
        dag_node (str): DAG node in the current scene.

    Returns:
        list[str]
    """

    return maya_fn.api.get_dag_path(dag_node).fullPathName()


def get_name(dag_node):
    """Return the name of the given dag node.

    Args:
        dag_node (str): DAG node in the current scene.

    Returns:
        list[str]
    """

    # Split the full path name because partial path name may not be unique.
    return maya_fn.api.get_dag_path(dag_node).fullPathName().split('|')[-1]


def get_parent(dag_node):
    """Return the parent of the given dag node.

    Args:
        dag_node (str): DAG path of a node in the current scene.

    Returns:
        str | None
    """

    dag_path = maya_fn.api.get_dag_path(dag_node)
    dag_path.pop()

    return dag_path.fullPathName() or None


def get_shapes(dag_node):
    """Return the shape nodes for the given node.

    Args:
        dag_node (str): DAG path of a transform in the current scene.

    Returns:
        list[str]
    """

    return [
        child.fullPathName()
        for child in _iter_children(dag_node)
        if child.node().hasFn(OpenMaya.MFn.kShape)
    ]


def _iter_children(dag_node):
    """Yield the children of the given node."""

    dag_path = maya_fn.api.get_dag_path(dag_node)

    for i in range(dag_path.childCount()):
        yield OpenMaya.MDagPath.getAPathTo(dag_path.child(i))
