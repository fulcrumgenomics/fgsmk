from collections import defaultdict
from pathlib import Path

from fgsmk.log import RuleLog


def test_rule_log_get_logs(datadir: Path) -> None:
    """Test parsing Snakemake log for rule logs."""
    snakemake_log: Path = datadir / "snakemake.log"
    logs = RuleLog.get_logs(snakemake_log=snakemake_log)

    assert len(logs) == 8

    rule_to_logs: defaultdict[str, list[Path | None]] = defaultdict(list)
    for log in logs:
        rule_to_logs[log.name].append(log.path)

    assert set(rule_to_logs.keys()) == {"single_log_file", "multiple_log_files", "no_log_file"}

    assert len(rule_to_logs["single_log_file"]) == 2
    assert (
        Path(Path.cwd() / "single_log_file.GCF_012345678.1.log") in rule_to_logs["single_log_file"]
    )
    assert (
        Path(Path.cwd() / "single_log_file.GCF_000987654.1.log") in rule_to_logs["single_log_file"]
    )

    for path in rule_to_logs["multiple_log_files"]:
        print(path)

    assert len(rule_to_logs["multiple_log_files"]) == 4
    assert (
        Path(Path.cwd() / "multiple_log_files.download.GCF_012345678.1.log")
        in rule_to_logs["multiple_log_files"]
    )
    assert (
        Path(Path.cwd() / "multiple_log_files.download.GCF_000987654.1.log")
        in rule_to_logs["multiple_log_files"]
    )
    assert (
        Path(Path.cwd() / "multiple_log_files.index.GCF_012345678.1.log")
        in rule_to_logs["multiple_log_files"]
    )
    assert (
        Path(Path.cwd() / "multiple_log_files.index.GCF_000987654.1.log")
        in rule_to_logs["multiple_log_files"]
    )

    assert rule_to_logs["no_log_file"] == [None, None]
