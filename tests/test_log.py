from collections import defaultdict
from glob import glob
from pathlib import Path

from fgsmk.log import RuleLog
from fgsmk.testing import run_snakemake


def test_rule_log_get_logs(datadir: Path, tmp_path: Path) -> None:
    """Test parsing Snakemake log for rule logs."""
    # Run the Snakefile with failing rules
    snakefile: Path = datadir / "failing_rules.smk"

    rules: dict[str, int] = {
        "all": 1,
        "single_log_file": 1,
        "total": 2,
    }

    run_snakemake(snakefile=snakefile, workdir=tmp_path, executor_name="local", rules=rules)

    snakemake_logs: list[str] = glob(str(tmp_path / ".snakemake/log/*.snakemake.log"))
    assert len(snakemake_logs) == 1
    logs = RuleLog.get_logs(base_path=tmp_path, snakemake_log=Path(snakemake_logs[0]))

    assert len(logs) == 8

    rule_to_logs: defaultdict[str, list[Path | None]] = defaultdict(list)
    for log in logs:
        rule_to_logs[log.name].append(log.path)

    assert set(rule_to_logs.keys()) == {"single_log_file", "multiple_log_files", "no_log_file"}

    assert len(rule_to_logs["single_log_file"]) == 2
    assert Path(tmp_path / "single_log_file.GCF_012345678.1.log") in rule_to_logs["single_log_file"]
    assert Path(tmp_path / "single_log_file.GCF_000987654.1.log") in rule_to_logs["single_log_file"]

    assert len(rule_to_logs["multiple_log_files"]) == 4
    assert (
        Path(tmp_path / "multiple_log_files.download.GCF_012345678.1.log")
        in rule_to_logs["multiple_log_files"]
    )
    assert (
        Path(tmp_path / "multiple_log_files.download.GCF_000987654.1.log")
        in rule_to_logs["multiple_log_files"]
    )
    assert (
        Path(tmp_path / "multiple_log_files.index.GCF_012345678.1.log")
        in rule_to_logs["multiple_log_files"]
    )
    assert (
        Path(tmp_path / "multiple_log_files.index.GCF_000987654.1.log")
        in rule_to_logs["multiple_log_files"]
    )

    assert rule_to_logs["no_log_file"] == [None, None]
