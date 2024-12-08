from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

Coord = tuple[int, int]


def add(coord1: Coord, coord2: Coord) -> Coord:
    x1, y1 = coord1
    x2, y2 = coord2

    return x1 + x2, y1 + y2


def subtract(coord1: Coord, coord2: Coord) -> Coord:
    x1, y1 = coord1
    x2, y2 = coord2

    return x1 - x2, y1 - y2


@dataclass
class AntennaMap:
    height: int
    width: int
    antenna_locations: dict[str, set[Coord]]

    @staticmethod
    def from_str(map_str: str) -> "AntennaMap":
        rows = map_str.split("\n")
        height = len(rows)
        width = len(rows[0])
        antenna_locations = defaultdict(set)
        for x in range(width):
            for y in range(height):
                if rows[y][x] == ".":
                    continue

                antenna_locations[rows[y][x]].add((x, y))

        return AntennaMap(height, width, antenna_locations)

    def count_antinodes(self) -> int:
        antinodes = set()
        for frequency, coords in self.antenna_locations.items():
            for coord1 in coords:
                for coord2 in coords:
                    if coord1 == coord2:
                        continue

                    coord_diff = subtract(coord2, coord1)
                    antinode1 = subtract(coord1, coord_diff)
                    if self.is_in_map(antinode1):
                        antinodes.add(antinode1)

                    antinode2 = add(coord2, coord_diff)
                    if self.is_in_map(antinode2):
                        antinodes.add(antinode2)

        return len(antinodes)

    def count_antinodes2(self) -> int:
        antinodes = set()
        for frequency, coords in self.antenna_locations.items():
            for coord1 in coords:
                for coord2 in coords:
                    if coord1 == coord2:
                        continue

                    coord_diff = subtract(coord2, coord1)
                    antinode_location = coord2
                    while self.is_in_map(antinode_location):
                        antinodes.add(antinode_location)
                        antinode_location = add(antinode_location, coord_diff)

                    antinode_location = coord1
                    while self.is_in_map(antinode_location):
                        antinodes.add(antinode_location)
                        antinode_location = subtract(antinode_location, coord_diff)

        return len(antinodes)

    def is_in_map(self, coord: Coord) -> bool:
        x, y = coord

        return 0 <= x < self.width and 0 <= y < self.height


def main() -> None:
    antenna_map_str = Path("input/input.txt").read_text("utf-8").strip()
    antenna_map = AntennaMap.from_str(antenna_map_str)

    print(
        f"{antenna_map.count_antinodes()} unique locations within the bounds of the map"
        " contain an antinode"
    )
    print(
        f"Using the updated model, {antenna_map.count_antinodes2()} unique locations"
        " within the bounds of the map contain an antinode"
    )


if __name__ == "__main__":
    main()
