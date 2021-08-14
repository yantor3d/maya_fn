"""Maya test suite config."""

import atexit
import os
import pytest

import maya.standalone

import maya_fn

maya.standalone.initialize()
atexit.register(maya.standalone.uninitialize)
