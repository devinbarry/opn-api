# OPN-API development

Notes for setting up development systems for the OPN API project.

## Create new local env

`python3.12 -m venv ~/venvs/opn-api`

## Install dependencies

1. Activate the venv
`source ~/venvs/opn-api/bin/activate`
2. Install package in development mode including dependencies
`pip install --upgrade -e ".[dev]"`

## Run tests locally on Merlin

1. Activate the venv
`source ~/venvs/opn-api/bin/activate`
2. Run the tests
`pytest`
3. Run the tests using unittest
`PYTHONPATH=src python -m unittest discover -s tests`


## Bump version & build package on local PyPI server

1. Update version string in __init__.py
2. Push to master and the package will be built.
3. Package is pushed to test pypi too

## Release to Production pypi.org

The build script checks for a matching git tag to ensure release to production.

3. `git tag -a v0.4.3 -m "Release v0.4.3"`
4. `git push origin master --tags`
