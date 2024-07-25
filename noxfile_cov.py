import nox


@nox.session(python=["3.11"], venv_backend="uv")
def cov_tests(session: nox.Session) -> None:
    args = session.posargs or ["--cov"]
    session.install("-r", "requirements_test.txt", "coverage[toml]")
    session.install("-e .")
    session.run("pytest", *args)


@nox.session(python="3.11", venv_backend="uv")
def coverage(session: nox.Session) -> None:
    """Upload coverage data."""
    session.install("codecov")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)
