import enum
import logging
from dataclasses import dataclass
from itertools import dropwhile
from pathlib import Path
from typing import Any
from typing import ClassVar

import attr
from fgpyo.io import assert_path_is_readable
from fgpyo.io import assert_path_is_writable

from fgsmk.io import __LINES_PER_LOGFILE
from fgsmk.io import _last_lines


@dataclass(frozen=True)
class RuleLog:
    """
    Stores the path and name for the log file for a rule.

    Attributes:
        path: the path to the log file for the rule
        name: the name of the rule
    """

    path: Path
    name: str

    RULE_ERROR_PREFIX: ClassVar[str] = "Error in rule "
    LOG_PREFIX: ClassVar[str] = "    log: "
    LOG_SUFFIX: ClassVar[str] = " (check log file(s) for error message)"

    @classmethod
    def get_logs(cls, snakemake_log: Path) -> list["RuleLog"]:
        """
        Gets the logs for the rules from a Snakemake log file.

        Args:
            snakemake_log: the path to the Snakemake log file

        Returns:
            a list of RuleLog instances, one for each failed rule invocation.
        """
        assert_path_is_readable(path=snakemake_log)
        lines: list[str] = snakemake_log.read_text().splitlines()

        logs: list[RuleLog] = []
        while lines:
            lines = list(
                dropwhile(lambda line: not line.startswith(cls.RULE_ERROR_PREFIX), iter(lines))
            )
            if lines:
                rule_name: str = lines[0][len(cls.RULE_ERROR_PREFIX) : -1]
                lines = list(
                    dropwhile(lambda line: not line.startswith(cls.LOG_PREFIX), iter(lines))
                )
                dir: Path = Path(".").absolute()
                log_path = dir / lines[0][len(cls.LOG_PREFIX) : -len(cls.LOG_SUFFIX)]
                lines = lines[1:]
                logs.append(RuleLog(path=log_path, name=rule_name))

        return logs


def _summarize_snakemake_errors(
    path: Path, lines_per_log: int | None = __LINES_PER_LOGFILE
) -> list[str]:
    """
    Summarizes any errors that occurred during a run of a pipeline.

    Uses the snakemake log to find all failed rule invocations and their log files. Produces a list
    of lines containing summary information per failed rule invocation and the last 50 lines of each
    log file.

    Notes:
        * fails if rule has more than one log file defined
        * fails if rule has no log file defined

    Args:
        path: the path to the main snakemake log file
        lines_per_log: the number of lines to pull from each log file, None to return all lines

    Returns:
        a list of lines containing summary information on all failed rule invocations
    """
    summary = []

    logs: list[RuleLog] = RuleLog.get_logs(snakemake_log=path)

    for log in logs:
        summary.append(f"========== Start of Error Info for {log.name} ==========")
        summary.append(f"Failed rule: {log.name}")
        summary.append(f"Last {lines_per_log} lines of log file: {log.path}")
        for line in _last_lines(path=log.path, max_lines=lines_per_log):
            summary.append(f"    {line}")
        summary.append(f"=========== End of Error Info for {log.name} ===========")

    return summary


def on_error(
    snakefile: Path,
    config: Any | None,
    log: Path,
    lines_per_log: int | None = __LINES_PER_LOGFILE,
) -> None:
    """
    Block of code that gets called if the snakemake pipeline exits with an error.

    The `log` variable contains a path to the snakemake log file which can be parsed for
    more information.  Summarizes information on failed jobs and writes it to the output
    and also to an error summary file in the working directory.

    Args:
        snakefile: the path to the snakefile
        config: the configuration for the pipeline
        log: the path to the snakemake log file
        lines_per_log: the number of lines to pull from each log file, None to return all lines
    """
    try:
        # Build the preface
        preface: list[str] = [
            "Error in snakemake pipeline.",
            f"working_dir = {Path('.').absolute()}",
        ]
        # print the config attributes
        if config is not None:
            try:
                for attribute in attr.fields(type(config)):
                    value = getattr(config, attribute.name)
                    if isinstance(value, enum.Enum):
                        value = value.value
                    else:
                        value = str(value)
                    preface.append(f"{attribute.name} = {value}")
            except Exception:
                try:
                    for key, value in config.items():
                        preface.append(f"{key} = {value}")
                except Exception:
                    preface.append(f"config = {config}")
        preface.append("Detailed error information follows.")

        summary = preface + _summarize_snakemake_errors(path=log, lines_per_log=lines_per_log)
        text = "\n".join(summary)
        pipeline_name = snakefile.with_suffix("").name
        logging.getLogger(pipeline_name).error(text)

        error_summary_file = Path("./error_summary.txt")
        assert_path_is_writable(path=error_summary_file)
        with error_summary_file.open("w") as out:
            out.write(text)
    except Exception as ex:
        print("###########################################################################")
        print("Exception raised in Snakemake onerror handler.")
        print(str(ex))
        print("###########################################################################")
