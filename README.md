# fgsmk

[![CI](https://github.com/fulcrumgenomics/fgsmk/actions/workflows/python_package.yml/badge.svg?branch=main)](https://github.com/fulcrumgenomics/fgsmk/actions/workflows/python_package.yml?query=branch%3Amain)
[![Python Versions](https://img.shields.io/badge/python-3.11_|_3.12-blue)](https://github.com/fulcrumgenomics/fgsmk)
[![MyPy Checked](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://docs.astral.sh/ruff/)

A set of utility functions for use in Snakemake workflows.

## Recommended Installation

This package is intended for use within a Snakemake workflow project.

Install the Python package and dependency management tool [`poetry`](https://python-poetry.org/docs/#installation) using official documentation.
You must have Python 3.11 or greater available on your system path, which could be managed by [`mamba`](https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html), [`pyenv`](https://github.com/pyenv/pyenv), or another package manager.

Install with `poetry` into the `mamba` environment for the parent project.

```console
poetry install --directory fgsmk
```

## Usage

### Error summary file

Set the `onerror` directive in a Snakemake workflow to point to the `fgsmk.on_error` function.

```
from fgsmk.log import on_error

onerror:
    on_error(snakefile=Path(__file__), config=config, log=Path(log))
    """Block of code that gets called if the snakemake pipeline exits with an error."""
```

This will produce a file `error_summary.txt` containing the last (up to) 50 lines of the log files of any rules that failed execution.
The content will also be output to `stdout`.

## Development and Testing

See the [contributing guide](./CONTRIBUTING.md) for more information.
