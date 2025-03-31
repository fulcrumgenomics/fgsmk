
[![Language][language-badge]][language-link]
[![Python Versions][python-versions-badge]][python-versions-link]
[![Code Style][code-style-badge]][code-style-link]
[![Type Checked][type-checking-badge]][type-checking-link]
[![PEP8][pep-8-badge]][pep-8-link]
[![Poetry][poetry-badge]][poetry-link]

---

[![License][license-badge]][license-link]
[![Python package][python-package-badge]][python-package-link]
[![PyPI version][pypi-badge]][pypi-link]
[![PyPI download total][pypi-downloads-badge]][pypi-downloads-link]

---
[language-badge]:        http://img.shields.io/badge/language-python-brightgreen
[language-link]:         http://www.python.org/
[python-versions-badge]: https://img.shields.io/badge/python-3.11_|_3.12-blue
[python-versions-link]:  https://github.com/fulcrumgenomics/fgsmk/blob/main/pyproject.toml
[code-style-badge]:      https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
[code-style-link]:       https://docs.astral.sh/ruff/
[type-checking-badge]:   http://www.mypy-lang.org/static/mypy_badge.svg
[type-checking-link]:    http://mypy-lang.org/
[pep-8-badge]:           https://img.shields.io/badge/code%20style-pep8-brightgreen
[pep-8-link]:            https://www.python.org/dev/peps/pep-0008/
[poetry-badge]:          https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json
[poetry-link]:           https://python-poetry.org/
[license-badge]:         https://img.shields.io/badge/license-MIT-blue
[license-link]:          https://github.com/fulcrumgenomics/fgsmk/blob/main/LICENSE
[python-package-badge]:  https://github.com/fulcrumgenomics/fgsmk/actions/workflows/python_package.yml/badge.svg?branch=main
[python-package-link]:   https://github.com/fulcrumgenomics/fgsmk/actions/workflows/python_package.yml
[pypi-badge]:            https://badge.fury.io/py/fgsmk.svg
[pypi-link]:             https://pypi.python.org/pypi/fgsmk
[pypi-downloads-badge]:  https://img.shields.io/pypi/dm/fgsmk
[pypi-downloads-link]:   https://pypi.python.org/pypi/fgsmk

# fgsmk

A set of utility functions for use in Snakemake workflows. Supports Snakemake 8+.

Table of Contents
=================

* [Recommended Installation](#recommended-installation)
* [Usage](#usage)
   * [Error summary file](#error-summary-file)
* [Development and Testing](#development-and-testing)

## Recommended Installation

This package is intended for use within a Snakemake workflow project.

Install the Python package and dependency management tool [`poetry`](https://python-poetry.org/docs/#installation) using official documentation.
You must have Python 3.11 or greater available on your system path, which could be managed by [`mamba`](https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html), [`pyenv`](https://github.com/pyenv/pyenv), or another package manager.

If you have a `mamba` environment for the parent project, activate it first.

Install with `poetry`.

```console
poetry install
```

## Usage

### Error summary file

Set the `onerror` directive in a Snakemake workflow to point to the `fgsmk.on_error` function.

```python
from fgsmk.log import on_error

onerror:
    on_error(snakefile=Path(__file__), config=config, log=Path(log))
    """Block of code that gets called if the snakemake pipeline exits with an error."""
```

This will produce a file `error_summary.txt` containing the last (up to) 50 lines of the log files of any rules that failed execution.
The content will also be output to `stdout`.

## Development and Testing

See the [contributing guide](./CONTRIBUTING.md) for more information.
