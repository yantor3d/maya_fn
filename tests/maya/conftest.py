"""Maya test suite config."""

import atexit
import os
import pytest

import maya.standalone

maya.standalone.initialize()
atexit.register(maya.standalone.uninitialize)

from maya import cmds


@pytest.fixture(scope="function")
def new_scene():
    """Open a new scene before running this test."""

    cmds.file(new=True, force=True)
