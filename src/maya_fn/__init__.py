"""Maya Function Set.

A set of wrappers around a set of maya.cmds and maya.api behaviors.
"""

import functools

from maya import cmds

import maya_fn.dg as dg  # noqa
import maya_fn.dag as dag  # noqa
import maya_fn.node as node  # noqa

from maya_fn.plug import plug  # noqa

__author__ = "Ryan Rorter"
__version__ = "0.0.1"
__license__ = "MIT"


def undoable(name):
    def wrapper(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            cmds.undoInfo(chunkName=name, openChunk=True)
            try:
                return func(*args, **kwargs)
            finally:
                cmds.undoInfo(closeChunk=True)
        return wrapped 
    return wrapper
