from pathlib import Path

import pytest

from fgsmk.io import _last_lines


@pytest.mark.parametrize(
    "lines,max_lines,expected_result",
    [
        (["line 1", "line 2", "line 3"], 2, ["line 2", "line 3"]),
        (["line 1", "line 2", "line 3"], 4, ["line 1", "line 2", "line 3"]),
        (["line 1", "line 2", "line 3"], None, ["line 1", "line 2", "line 3"]),
    ],
)
def test_read_last_lines(
    tmp_path: Path, lines: list[str], max_lines: int | None, expected_result: list[str]
) -> None:
    """Test reading the last lines from a file."""
    file: Path = tmp_path / "test.txt"
    file.write_text("\n".join(lines))
    last: list[str] = _last_lines(path=file, max_lines=max_lines)

    assert last == expected_result, "Last lines did not match expected last lines."


def test_read_last_lines_no_file_error(tmp_path: Path) -> None:
    """Test reading the last lines from a non-existent file."""
    last: list[str] = _last_lines(path=tmp_path / "non_existent.txt", max_lines=50)

    assert last[0].startswith(">>> Could not open log file for reading")


def test_read_last_lines_non_positive_max_lines_error(tmp_path: Path) -> None:
    """Test reading the last lines with a non-positive max_lines value."""
    lines: list[str] = ["line 1", "line 2", "line 3"]
    file: Path = tmp_path / "test.txt"
    file.write_text("\n".join(lines))
    with pytest.raises(ValueError, match="Number of lines requested must be > 0. Saw 0"):
        _last_lines(path=file, max_lines=0)
