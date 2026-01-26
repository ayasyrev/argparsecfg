import nox


@nox.session(python=["3.10", "3.11", "3.12", "3.13", "3.14"], venv_backend="uv")
def cov_tests(session: nox.Session) -> None:
    args = session.posargs or ["--cov"]
    session.run("uv", "pip", "install", "--group", "test", "-e", ".")
    session.run("pytest", *args)


@nox.session(python="3.14", venv_backend="uv")
def coverage(session: nox.Session) -> None:
    """Upload coverage data."""
    session.run("uv", "pip", "install", "codecov")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)
