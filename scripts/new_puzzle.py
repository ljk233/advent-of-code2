"""new_puzzle.py"""

import sys
from pathlib import Path

from loguru import logger

SAMPLES_DIR = "samples"
INPUTS_DIR = "inputs"
PUZZLES_DIR = "puzzles"


def main(year: int, day: int) -> None:
    root = Path()
    day_str = f"{day:02d}"
    puzzle_dir = root / PUZZLES_DIR / str(year)
    data_dirs = [root / data_dir / str(year) for data_dir in [INPUTS_DIR, SAMPLES_DIR]]

    # Create the directories
    for directory in [puzzle_dir] + data_dirs:
        directory.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created directory: {directory.relative_to(root)}")

    # Create the puzzle solution file
    puzzle_path = puzzle_dir / f"{day_str}.py"
    if not puzzle_path.exists():
        puzzle_content = (
            Path("templates/solve.txt")
            .read_text()
            .replace(r"{{YEAR}}", str(year))
            .replace(r"{{DAY}}", f"{day}")
        )
        puzzle_path.write_text(puzzle_content)
        logger.info(f"Created solution file: {puzzle_path}")

    # Touch the data files
    for data_dir in data_dirs:
        data_path = data_dir / f"{day_str}.txt"
        if not data_path.exists():
            data_path.touch()
            logger.info(f"Created file: {data_path}")


if __name__ == "__main__":
    try:
        main(int(sys.argv[1]), int(sys.argv[2]))
    except IndexError:
        logger.error(f"Usage: python new_puzzle.py <year> <day> (Not {sys.argv})")
