"""
Tests for snakemake pipelines.

The tests briefly test the Snakefiles to ensure they are runnable and generally execute the
expected rules.  They are far from comprehensive, as they do not verify the analytical results
of each pipeline, which should be done elsewhere.
"""

from collections import defaultdict
from pathlib import Path
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional

from snakemake.api import SnakemakeApi
from snakemake.settings.types import ConfigSettings
from snakemake.settings.types import ExecutionSettings
from snakemake.settings.types import OutputSettings
from snakemake.settings.types import Quietness
from snakemake.settings.types import ResourceSettings
from snakemake_interface_executor_plugins.registry import ExecutorPluginRegistry


class SnakemakeLogger(object):
    """Returns a log handler for snakemake and tracks if the rules that were run."""

    def __init__(self) -> None:
        """Builds a new logger."""
        self.rule_count: Dict[str, int] = defaultdict(lambda: 0)

    def log_handler(self) -> Callable[[Dict[str, Any]], None]:
        """Returns a log handler for use with snakemake."""

        def fn(d: Dict[str, Any]) -> None:
            if d["level"] != "run_info":
                return
            # NB: skip the first three, and skip the last, lines
            for counts_line in d["msg"].split("\n")[3:-1]:
                counts_line = counts_line.strip()
                job, count = counts_line.split()
                assert int(count) > 0, counts_line

                self.rule_count[job] += int(count)

        return fn


def run_snakemake(
    snakefile: Path,
    workdir: Path,
    rules: Dict[str, int],
    config: Optional[Dict[str, Any]] = None,
    configfiles: Optional[List[Path]] = None,
    quiet: bool = True,
) -> SnakemakeLogger:
    """
    Runs Snakemake.

    Args:
        snakefile: the snake file to execute
        workdir: the working directory in which to run Snakemake
        rules: a mapping of rule name to expect # of times it should run
        config: the optional configuration object for Snakemake
        configfiles: the optional list of configuration files for Snakemake
        quiet: tells snakemake to not output logging, set to true for debugging failing pipelines
    """
    assert snakefile.is_file(), f"{snakefile} is not a file"
    assert snakefile.exists(), f"{snakefile} does not exist"

    logger = SnakemakeLogger()
    quietness = None if quiet else {Quietness.ALL}

    executor_plugin = ExecutorPluginRegistry().get_plugin("dryrun")
    executor_settings = executor_plugin.get_settings([])

    with SnakemakeApi(
        OutputSettings(
            quiet=quietness,
            log_handlers=[logger.log_handler()],
            keep_logger=False,
            stdout=True,
        )
    ) as snakemake_api:
        workflow_api = snakemake_api.workflow(
            resource_settings=ResourceSettings(
                resources={"mem_gb": 8},
            ),
            config_settings=ConfigSettings(
                config=config,
                configfiles=[] if configfiles is None else configfiles,
                config_args={},
            ),
            snakefile=snakefile,
            workdir=workdir,
        )

        dag_api = workflow_api.dag()

        dag_api.execute_workflow(
            executor="dryrun",
            execution_settings=ExecutionSettings(
                standalone=True,
                ignore_ambiguity=True,
            ),
            executor_settings=executor_settings,
        )

    # check the "all" rule
    assert logger.rule_count["all"] == 1, (
        f"All rule was not run once, found: {logger.rule_count['all']}"
    )

    # check that the executed rules were run the correct # of times
    for rule, count in logger.rule_count.items():
        assert rule in rules, f"Could not find {rule} in {rules}"
        assert count == rules[rule], f"{rule}: {rules[rule]}"

    # check that all the expected rules were run
    for rule in rules:
        assert rule in logger.rule_count

    return logger
