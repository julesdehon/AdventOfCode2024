from pathlib import Path
from typing import Optional

Coordinate = tuple[int, int]
CoordinateSequence = list[Coordinate]
Grid = list[str]

UPWARD_RIGHT_DIAGONAL_MAS_SEARCHES: list[CoordinateSequence] = [
    [(-1, -1), (0, 0), (1, 1)],
    [(1, 1), (0, 0), (-1, -1)],
]

DOWNWARD_RIGHT_DIAGONAL_MAS_SEARCHES: list[CoordinateSequence] = [
    [(1, -1), (0, 0), (-1, 1)],
    [(-1, 1), (0, 0), (1, -1)],
]

XMAS_SEARCH_DIRECTIONS: list[Coordinate] = [
    (0, 1),
    (0, -1),
    (1, 1),
    (1, -1),
    (1, 0),
    (-1, 0),
    (-1, -1),
    (-1, 1),
]

XMAS_SEARCHES: list[CoordinateSequence] = [
    [(i * dx, i * dy) for i in range(4)] for dx, dy in XMAS_SEARCH_DIRECTIONS
]


def apply_search(
    x: int, y: int, search: list[CoordinateSequence]
) -> list[CoordinateSequence]:
    return [[(x + dx, y + dy) for dx, dy in offsets] for offsets in search]


def get_potential_word(coords: CoordinateSequence, grid: Grid) -> Optional[str]:
    word = ""
    for x, y in coords:
        if x < 0 or y < 0 or y >= len(grid) or x >= len(grid[y]):
            return None
        word += grid[y][x]
    return word


def count_xmas_patterns(x: int, y: int, grid: Grid) -> int:
    count = 0
    for pattern in apply_search(x, y, XMAS_SEARCHES):
        potential_word = get_potential_word(pattern, grid)
        if potential_word == "XMAS":
            count += 1
    return count


def count_xmas_cross_patterns(x: int, y: int, grid: Grid) -> int:
    found_upward_right_mas = any(
        get_potential_word(pattern, grid) == "MAS"
        for pattern in apply_search(x, y, UPWARD_RIGHT_DIAGONAL_MAS_SEARCHES)
    )
    found_downward_right_mas = any(
        get_potential_word(pattern, grid) == "MAS"
        for pattern in apply_search(x, y, DOWNWARD_RIGHT_DIAGONAL_MAS_SEARCHES)
    )

    return 1 if found_upward_right_mas and found_downward_right_mas else 0


def main() -> None:
    grid: Grid = [
        line.strip()
        for line in Path("input/input.txt").read_text("utf-8").split("\n")
        if line.strip() != ""
    ]

    total_xmas_patterns = 0
    total_xmas_cross_patterns = 0

    for y, row in enumerate(grid):
        for x in range(len(row)):
            total_xmas_patterns += count_xmas_patterns(x, y, grid)
            total_xmas_cross_patterns += count_xmas_cross_patterns(x, y, grid)

    print(f"Total 'XMAS' patterns: {total_xmas_patterns}")
    print(f"Total 'XMAS Cross' patterns: {total_xmas_cross_patterns}")


if __name__ == "__main__":
    main()
