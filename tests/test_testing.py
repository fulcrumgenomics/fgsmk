from pathlib import Path
from typing import Dict

from fgsmk.testing import run_snakemake


def test_hello_world(datadir: Path, tmp_path: Path) -> None:
    """Basic unit test that runs the snakefile in dry-run mode to ensure it parses correctly."""
    snakefile: Path = datadir / "hello_world.smk"

    rules: Dict[str, int] = {
        "all": 1,
        "hello_world": 1,
        "total": 2,
    }

    run_snakemake(snakefile=snakefile, workdir=tmp_path, rules=rules)
