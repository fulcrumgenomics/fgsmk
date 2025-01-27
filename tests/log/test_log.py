from pathlib import Path

from fgsmk.log import RuleLog


def test_rule_log_get_logs(datadir: Path) -> None:
    """Test parsing Snakemake log for rule logs."""
    snakemake_log: Path = datadir / "snakemake.log"
    logs = RuleLog.get_logs(snakemake_log=snakemake_log)

    assert len(logs) == 3

    assert {rule.name for rule in logs} == {"download_genomes"}

    paths: set[str] = {str(rule.path) for rule in logs}
    assert str(Path.cwd() / "logs/download_genomes.GCF_012345678.1.log") in paths
    assert str(Path.cwd() / "logs/download_genomes.GCF_000987654.1.log") in paths
    assert str(Path.cwd() / "logs/download_genomes.GCF_023232323.1.log") in paths
