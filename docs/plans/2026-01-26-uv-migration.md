# UV Migration Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Migrate packaging to `uv` with `pyproject.toml`, support Python 3.10–3.14, and consolidate dependencies as loose specifiers.

**Architecture:** Replace `setup.cfg`/`setup.py` + `requirements_*.txt` with a PEP 621 `pyproject.toml` using a modern build backend. Centralize runtime dependencies and use optional dependency groups for dev/test/docs, then generate a `uv.lock` for reproducibility.

**Tech Stack:** Python, uv, setuptools (build backend), nox.

---

### Task 1: Add PEP 621 `pyproject.toml`

**Files:**
- Create: `pyproject.toml`
- Modify: `README.md` (optional note about uv usage)

**Step 1: Draft `pyproject.toml` with metadata**

```toml
[build-system]
requires = ["setuptools>=68.2.0,<80.0.0", "wheel>=0.41.0"]
build-backend = "setuptools.build_meta"

[project]
name = "argparsecfg"
dynamic = ["version"]
description = "argparse config."
readme = "README.md"
requires-python = ">=3.10,<3.15"
authors = [{name = "Yasyrev Andrei", email = "a.yasyrev@gmail.com"}]
license = {text = "Apache-2.0"}
classifiers = [
  "Programming Language :: Python :: 3",
  "Programming Language :: Python :: 3.10",
  "Programming Language :: Python :: 3.11",
  "Programming Language :: Python :: 3.12",
  "Programming Language :: Python :: 3.13",
  "Programming Language :: Python :: 3.14",
  "License :: OSI Approved :: Apache Software License",
  "Operating System :: OS Independent",
]

[project.dependencies]
# (currently none)

[project.optional-dependencies]
dev = [
  "black",
  "black[jupyter]",
  "coverage[toml]",
  "flake8",
  "isort",
  "mypy",
  "nbmetaclean",
  "nox",
  "pre-commit",
  "pytest",
  "pytest-cov",
  "ruff",
]
test = [
  "pytest",
  "pytest-cov",
]
docs = [
  "nbdocs",
]

[tool.setuptools]
package-dir = { "" = "src" }

[tool.setuptools.packages.find]
where = ["src"]
exclude = ["tests*", "Nbs*", "docs*"]

[tool.setuptools.dynamic]
version = { attr = "argparsecfg.version.__version__" }
```

**Step 2: Add uv config to allow prerelease resolution**

```toml
[tool.uv]
prerelease = "allow"
```

**Step 3: Commit**

```bash
git add pyproject.toml
git commit -m "chore: add pyproject.toml for uv packaging"
```

---

### Task 2: Update tooling for Python 3.10–3.14

**Files:**
- Modify: `noxfile.py`

**Step 1: Update nox Python versions**

```python
@nox.session(python=["3.10", "3.11", "3.12", "3.13", "3.14"], venv_backend="uv")
```

**Step 2: Run a single session locally (optional)**

Run: `nox -s tests -p 3.12`
Expected: tests pass.

**Step 3: Commit**

```bash
git add noxfile.py
git commit -m "chore: update nox python versions"
```

---

### Task 3: Remove legacy packaging files

**Files:**
- Delete: `setup.cfg`
- Delete: `setup.py`
- Delete: `requirements.txt`
- Delete: `requirements_dev.txt`
- Delete: `requirements_test.txt`
- Delete: `requirements_docs.txt`

**Step 1: Delete legacy files**

Run: `rm setup.cfg setup.py requirements*.txt`

**Step 2: Ensure docs don’t reference removed files**

Run: `rg "requirements_.*\\.txt|setup\\.cfg|setup\\.py" -n`
Expected: No relevant references remain, or update docs/README to match.

**Step 3: Commit**

```bash
git add -u
git commit -m "chore: remove legacy packaging files"
```

---

### Task 4: Generate uv lockfile

**Files:**
- Create: `uv.lock`

**Step 1: Generate the lockfile**

Run: `uv lock`
Expected: `uv.lock` created.

**Step 2: Commit**

```bash
git add uv.lock
git commit -m "chore: add uv lockfile"
```

---

### Task 5: Verify packaging + tests

**Files:**
- None

**Step 1: Build the package**

Run: `uv build`
Expected: wheel/sdist built without errors.

**Step 2: Run tests**

Run: `uv run pytest`
Expected: tests pass.

**Step 3: Commit (if changes occurred)**

```bash
git add -u
git commit -m "chore: verify build and tests"
```
