# Publishing xlocllm

This checklist publishes `xlocllm` so users can install it with:

```powershell
pip install xlocllm
```

## 1. One-Time Accounts

Create or confirm access to:

- GitHub repository: `https://github.com/mgg789/xlocllm`
- TestPyPI account: `https://test.pypi.org`
- PyPI account: `https://pypi.org`

Recommended PyPI security setup:

- Enable 2FA on PyPI.
- Create a project-scoped API token after the first upload.
- For the first upload, use an account token if a project-scoped token cannot
  exist yet.

## 2. Local Tools

From the repository root:

```powershell
python -m pip install --upgrade pip
python -m pip install -e .\python\xlocllm[dev,openai]
```

The `dev` extra installs:

- `pytest`
- `ruff`
- `mypy`
- `httpx`
- `build`
- `twine`

## 3. Verify Package Metadata

Check `python/xlocllm/pyproject.toml`:

- `name = "xlocllm"`
- `version = "1.0.0"`
- `readme = "README.md"`
- repository URLs point to `https://github.com/mgg789/xlocllm`
- `src/xlocllm/webui` is included in the wheel
- `src/xlocllm/data/models.json` is included in the wheel
- `src/xlocllm/py.typed` is included in the wheel

Every release must use a new version. PyPI does not allow replacing an already
uploaded version.

## 4. Run Checks

From the repository root:

```powershell
python -m pytest python/xlocllm/tests
python -m ruff check python/xlocllm/src python/xlocllm/tests
python -m mypy python/xlocllm/src
```

Optional web checks:

```powershell
pnpm install
pnpm build
pnpm test
```

## 5. Build Distributions

```powershell
cd python\xlocllm
Remove-Item -Recurse -Force dist -ErrorAction SilentlyContinue
python -m build
python -m twine check dist/*
```

Expected files:

- `dist/xlocllm-1.0.0-py3-none-any.whl`
- `dist/xlocllm-1.0.0.tar.gz`

## 6. Inspect Wheel Contents

```powershell
python - <<'PY'
from pathlib import Path
from zipfile import ZipFile

wheel = next(Path("dist").glob("*.whl"))
with ZipFile(wheel) as archive:
    names = set(archive.namelist())
    required = [
        "xlocllm/py.typed",
        "xlocllm/data/models.json",
        "xlocllm/webui/index.html",
    ]
    missing = [name for name in required if name not in names]
    if missing:
        raise SystemExit(f"Missing from wheel: {missing}")
    print(f"OK: {wheel}")
PY
```

## 7. Publish To TestPyPI

```powershell
python -m twine upload --repository testpypi dist/*
```

Install from TestPyPI in a clean environment. Use `--extra-index-url` so normal
dependencies still resolve from PyPI:

```powershell
python -m venv .venv-test-xlocllm
.\.venv-test-xlocllm\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple "xlocllm[openai]"
python - <<'PY'
import xlocllm
print(xlocllm.model("Qwen-3.5-0.8b", unit="LLM").model_id)
print(xlocllm.runtime([xlocllm.unit("LLM", "Qwen-3.5-0.8b")]).url)
PY
deactivate
```

## 8. Publish To PyPI

After TestPyPI install works:

```powershell
cd python\xlocllm
python -m twine upload dist/*
```

Then verify:

```powershell
python -m venv .venv-pypi-xlocllm
.\.venv-pypi-xlocllm\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install "xlocllm[openai]"
python - <<'PY'
import xlocllm
print(xlocllm.__all__)
print(xlocllm.model("Qwen-3.5-0.8b", unit="LLM").model_id)
PY
deactivate
```

## 9. GitHub Repository

If the repository does not exist yet:

```powershell
winget install --id GitHub.cli
gh auth login
gh repo create mgg789/xlocllm --public --source . --remote origin --push
```

If the repository already exists:

```powershell
git init
git branch -M main
git remote add origin https://github.com/mgg789/xlocllm.git
git add .
git commit -m "Release xlocllm 1.0.0"
git push -u origin main
```

If this repository remains a monorepo, run those commands from the repository
root. If you want a Python-package-only repository, copy these paths into a clean
folder first:

- `python/xlocllm/src`
- `python/xlocllm/tests`
- `python/xlocllm/README.md`
- `python/xlocllm/docs.md`
- `python/xlocllm/docs_ru.md`
- `python/xlocllm/models.md`
- `python/xlocllm/models_ru.md`
- `python/xlocllm/PUBLISHING.md`
- `python/xlocllm/pyproject.toml`
- `LICENSE`

## 10. Release Checklist

- Version bumped in `pyproject.toml`.
- Tests, Ruff, and mypy pass.
- `python -m build` succeeds.
- `python -m twine check dist/*` passes.
- Wheel includes `webui`, `models.json`, and `py.typed`.
- TestPyPI install works.
- PyPI upload succeeds.
- GitHub tag created:

```powershell
git tag v1.0.0
git push origin v1.0.0
```

Official references:

- Python Packaging User Guide: `https://packaging.python.org`
- Twine: `https://twine.readthedocs.io`
- PyPI project metadata: `https://docs.pypi.org/project_metadata/`
