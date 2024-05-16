# PyCon US 2024

## Fundamentals of API Security with Python

### By Jose Haro Peralta

Welcome to the tutorial!

This repository contains a vulnerable API. During the tutorial, we'll anlayze how it's vulnerable,
how we exploit its vulnerabilities, and how we fix them.

---

### Installing dependencies

The first step is installing the dependencies. The repo ships with a pyproject and a poetry.lock files.
If you use Poetry, you can install the dependencies from those files.

The minimum Python version indicated in pyproject.toml is 3.8. It may work with previous versions but not 
guaranteed. I've only tested with 3.10.

If you don't use poetry, feel free to install the dependencies with pipenv, or alternatively create 
a virtual environment using venv or a similar tool, and install with pip.

This is the list of dependencies:

- fastapi = "^0.111.0"
- uvicorn = "^0.29.0"
- python-jose = "^3.3.0"
- sqlalchemy = "^2.0.30"
- requests = "^2.31.0"

### Adding configuration

To run the server, we need to add some configuration in auth/auth_api.py. 
Starting in [line 10](https://github.com/abunuwas/pycon-us-2024/blob/main/auth/auth_api.py#L10),
the need the values of the following variables:

```python
client_id = os.getenv("auth0_client_id")
client_secret = os.getenv("auth0_client_secret")
authorizer_url = os.getenv("auth0_domain")
```

The values will be provided during the tutorial.

### Running the server

To run the server, use the following command:

``` bash
uvicorn server:server --reload
```
