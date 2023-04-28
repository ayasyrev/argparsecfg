from pathlib import Path

import nox

example_files = list(Path("examples").glob("example*.py"))
print(example_files)


@nox.session(python=["3.7", "3.8", "3.9", "3.10", "3.11"], venv_backend="mamba")
def tests(session: nox.Session) -> None:
    session.conda_install("--file", "requirements_test.txt")
    session.install("-e", ".")
    for filename in example_files:
        session.run("python", str(filename))