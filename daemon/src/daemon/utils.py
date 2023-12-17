import os


def get_secret(name: str) -> str:
    file = get_env_variable(name)
    if not os.path.isfile(file):
        raise FileNotFoundError(f"Secret file {file} not found")
    with open(file, "r") as f:
        secret = f.read()
    return secret


def get_env_variable(name: str) -> str:
    var = os.getenv(name)
    if var:
        return var
    else:
        raise FileNotFoundError(f"Environment variable {name} not set")
