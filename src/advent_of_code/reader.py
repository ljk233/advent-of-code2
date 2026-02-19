"""reader.py"""

from pathlib import Path

DATA_DIR = Path() / "data"
INPUT_DIR = Path() / "inputs"
SAMPLE_DIR = Path() / "samples"


def read_lines(year: int, day: int, test: bool = False) -> list[str]:
    line = read(year, day, test)

    return line.splitlines()


def read(year: int, day: int, test: bool = False) -> str:
    day_str = f"{day:02d}"
    file = "sample.txt" if test else "input.txt"
    path = DATA_DIR / str(year) / day_str / file

    return path.read_text()


def read_lines2(
    year: int, day: int, test: bool = False, test_num: int = 1
) -> list[str]:
    return read2(year, day, test=test, test_num=test_num).splitlines()


def read2(year: int, day: int, test: bool = False, test_num: int = 1) -> str:
    day_str = f"{day:02d}"
    if test and test_num >= 2:
        day_str += f"_{test_num}"

    file = f"{day_str}.txt"
    dir_path = SAMPLE_DIR if test else INPUT_DIR
    path = dir_path / str(year) / file

    return path.read_text()
