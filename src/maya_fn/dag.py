"""DAG node utilities."""

from maya import cmds
from maya.api import OpenMaya

import maya_fn.api

__all__ = [
    "ancestors",
    "children",
    "descendents",
    "full_path",
    "name",
    "parent",
    "path",
    "shapes",
    "siblings",
]


def ancestors(dag_node):
    """Return the ancestors of the given dag node, depth first.

    Args:
        dag_node (str): DAG node in the current scene.

    Returns:
        list[str]
    """

    return list(_iter_parents(dag_node))[::-1]


def child(dag_node, dag_name):
    """Return the child of the given dag node."""

    return dag_node + '|' + dag_name


def children(dag_node):
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


def descendents(dag_node):
    """Yield the descendents of the given dag node, depth first.

    Args:
        dag_node (str): DAG node in the current scene.

    Yields:
        str
    """

    for child in children(dag_node):
        yield child

        for each in descendents(child):
            yield each


def full_path(dag_node):
    """Return the full path of the given dag node.

    Args:
        dag_node (str): DAG node in the current scene.

    Returns:
        str
    """

    return maya_fn.api.get_dag_path(dag_node).fullPathName()


get = maya_fn.api.get_dag_path


def name(dag_node):
    """Return the name of the given dag node.

    Args:
        dag_node (str): DAG node in the current scene.

    Returns:
        str
    """

    # Split the full path name because partial path name may not be unique.
    return maya_fn.api.get_dag_path(dag_node).fullPathName().split("|")[-1]


def parent(dag_node):
    """Return the parent of the given dag node.

    Args:
        dag_node (str): DAG path of a node in the current scene.

    Returns:
        str | None
    """

    dag_path = maya_fn.api.get_dag_path(dag_node)
    dag_path.pop()

    return dag_path.fullPathName() or None


def partial_path(dag_node):
    """Return the partial path of the given dag node.

    Args:
        dag_node (str): DAG node in the current scene.

    Returns:
        list[str]
    """

    return maya_fn.api.get_dag_path(dag_node).partialPathName()


path = maya_fn.api.get_dag_path


def shapes(dag_node):
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


def siblings(dag_node):
    """Return the siblings of the given dag node.

    Args:
        dag_node (str): DAG node in the current scene.

    Returns:
        list[str]
    """

    dag_path = path(dag_node)

    _parent = parent(dag_node)

    if not _parent:
        _siblings = cmds.ls(assemblies=True, long=True)
    else:
        _siblings = [each.fullPathName() for each in _iter_children(_parent)]

    _siblings.remove(dag_path.fullPathName())

    return _siblings


def _iter_children(dag_node):
    """Yield the children of the given node."""

    dag_path = maya_fn.api.get_dag_path(dag_node)

    for i in range(dag_path.childCount()):
        yield OpenMaya.MDagPath.getAPathTo(dag_path.child(i))


def _iter_parents(dag_node):
    """Yield the children of the given node."""

    dag_path = maya_fn.api.get_dag_path(dag_node)

    while dag_path.length():
        dag_path = dag_path.pop()

        if dag_path.length():
            yield dag_path.fullPathName()
        else:
            break
