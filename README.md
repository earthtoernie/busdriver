__creating a virtual environment__

1. if have a venv that is messed up, run `deactivate` then delete `venv` folder.
3. create the virtual environment in a folder called `venv`
`python3 -m venv venv`
4. `source venv/bin/activate`
5. `pip install --upgrade setuptools` always run this to update setuptools local to the venv
6. `pip install -e .`
