# Maya Pocket Tools (maya_fn)
A set of wrappers around a set of maya.cmds and maya.api behaviors. 

# Tests
The recommended approach for running tests is to setup a virtual environment. Edit the `activate.bat` script to include the `/src` directory and set a `MAYA_LOCATION` environment variable, as shown below.

```
python -m virtualenv venv
venv\Scripts\activate.bat
pip install -r requirements/dev.txt
```

```
# activate.bat
set "PYTHONPATH=%VIRTUAL_ENV%\..\src"
set "MAYA_LOCATION=C:\Program Files\Autodesk\Maya2020"
```

You can execute the following `tox` environments:

 - `tox` runs all environments, including: `maya`
 - `tox -e maya` runs the maya tests
 - `tox -e black` runs Black on the code.
 - `tox -e lint` runs flake8 and pydocstyles on the code.
