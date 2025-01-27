################################################################################
# A workflow designed to fail.
#
# snakemake -j4 -k -s tests/data/failing_rules.smk --directory tests/data
#
# The Snakemake log file tests/data/snakemake.log is a copy of the output from
# e.g. tests/data/.snakemake/log/2025-01-27T124222.108734.snakemake.log
#
# The -k flag is to "Go on with independent jobs if a job fails."
################################################################################

accessions: list[str] = ["GCF_012345678.1", "GCF_000987654.1"]


rule all:
    input:
        expand("{accession}.single_log_file_output.txt", accession=accessions),
        expand("{accession}.multiple_log_file_output.txt", accession=accessions),
        expand("{accession}.no_log_file_output.txt", accession=accessions),


rule single_log_file:
    """A rule that always fails and has a single log file."""
    output:
        "{accession}.single_log_file_output.txt",
    log:
        "single_log_file.{accession}.log",
    shell:
        """
        (
            false
        ) &> {log}
        """


rule multiple_log_files:
    """A rule that always fails and has multiple log files."""
    output:
        "{accession}.multiple_log_file_output.txt",
    log:
        download="multiple_log_files.download.{accession}.log",
        index="multiple_log_files.index.{accession}.log",
    shell:
        """
        (
            false
        ) &> {log.download}

        (
            false
        ) &> {log.index}
        """


rule no_log_file:
    """A rule that always fails and has no log file."""
    output:
        "{accession}.no_log_file_output.txt",
    shell:
        """
        false
        """
