import nox


@nox.session(python=["3.11", "3.12", "3.13", "3.14"], venv_backend="uv")
def tests(session: nox.Session) -> None:
    args = session.posargs or ["--cov"]
    session.run("uv", "pip", "install", "--group", "test", "-e", ".")
    session.run("pytest", *args)
