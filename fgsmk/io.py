from pathlib import Path
from typing import Iterable
from typing import Optional

__LINES_PER_LOGFILE: int = 50
"""The default number of lines to return from the log files for each failed job."""


def read_lines(path: Path) -> list[str]:
    """
    Reads a file and returns it as a list of lines with newlines stripped.

    Args:
        path: the path of the file to read
    Return:
        the list of lines from the file
    """
    with path.open("r") as fh:
        lines: list[str] = fh.readlines()
        return [line.rstrip() for line in lines]


def write_lines(path: Path, lines: Iterable[str]) -> None:
    """
    Writes a list of lines to a file with newlines between the lines.

    Args:
        path:  the path to write to
        lines: the list of lines to write
    """
    with path.open("w") as out:
        for line in lines:
            out.write(line)
            out.write("\n")


def last_lines(path: Path, max_lines: Optional[int] = __LINES_PER_LOGFILE) -> list[str]:
    """
    Returns the last N lines from a file as a list.

    Args:
        path: the path to the file (must exist)
        max_lines: the number of line to return, None will return all lines
    Return:
        the last n lines of the file as a list, or the whole file < n lines.

    Raises:
        ValueError: If the number of lines requested is <= 0.
    """
    if max_lines <= 0:
        raise ValueError(f"Number of lines requested must be > 0. Saw {max_lines}.")

    try:
        lines: list[str] = read_lines(path)
        if max_lines is not None and len(lines) > max_lines:
            lines = lines[-max_lines : len(lines)]
        return lines
    except Exception:
        return [f">>> Could not open log file for reading: {path}. <<<"]
