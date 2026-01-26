import nox

locations = "."


@nox.session(python=["3.10", "3.11", "3.12", "3.13", "3.14"], venv_backend="mamba")
def conda_lint(session: nox.Session) -> None:
    args = session.posargs or locations
    session.conda_install("ruff")
    session.run("ruff", "check", *args)
