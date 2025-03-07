from pathlib import Path
from typing import Dict

from fgsmk.testing import run_snakemake


def test_hello_world(tmp_path) -> None:
    """Basic unit test that runs the snakefile in dry-run mode to ensure it parses correctly."""
    snakefile = Path(__file__).parent / "data" / "hello_world.smk"

    rules: Dict[str, int] = {
        "all": 1,
        "hello_world": 1,
    }

    run_snakemake(snakefile=snakefile, workdir=tmp_path, rules=rules)
