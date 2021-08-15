"""Maya API functions."""

from maya.api import OpenMaya


__all__ = [
    "get_dag_path",
    "get_object",
    "get_plug",
]


def get_dag_path(obj):
    """Return the MDagPath of the given object.

    Args:
        obj (Any): An object in the current Maya scene.

    Returns:
        maya.api.OpenMaya.MDagPath

    Raises:
        LookupError: If the given object does not exist.
        TypeError: If the given object is not a DAG node.
        ValueError: If the given object is not selectable.
    """

    dag = get_object(obj)

    try:
        return OpenMaya.MDagPath.getAPathTo(dag)
    except RuntimeError:
        raise TypeError("Object '{}' is not a DAG node.".format(obj))


def get_object(obj):
    """Return the MObject of the given object.

    Args:
        obj (Any): An object in the current Maya scene.

    Returns:
        maya.api.OpenMaya.MObject

    Raises:
        LookupError: If the given object does not exist.
        ValueError: If the given object is not selectable.
    """

    return _get_selection(obj).getDependNode(0)


def get_plug(obj):
    """Return the MPlug of the given plug.

    Args:
        obj (Any): A plug in the current Maya scene.

    Returns:
        maya.api.OpenMaya.MPlug

    Raises:
        LookupError: If the given object does not exist.
        TypeError: If the given object is not a plug.
        ValueError: If the given object is not selectable.
    """

    try:
        return _get_selection(obj).getPlug(0)
    except TypeError:
        raise TypeError("Object '{}' is not a plug.".format(obj))


def _get_selection(obj):
    """Return a selection list for the given object."""

    sel = OpenMaya.MSelectionList()

    try:
        sel.add(obj)
    except RuntimeError:
        raise LookupError("Object '{}' does not exist.".format(obj))
    except TypeError:
        raise ValueError(
            "Cannot select a(n) {} object '{}' - "
            "expected a string, MObject, MDagPath, or MPlug.".format(
                type(obj).__name__, obj
            )
        )

    return sel
