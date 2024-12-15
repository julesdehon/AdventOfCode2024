from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import FrozenSet

Coord = tuple[int, int]

X = 0
Y = 1


class EdgeSide(Enum):
    LEFT = 0
    TOP = 1
    RIGHT = 2
    BOTTOM = 3


@dataclass(frozen=True)
class Edge:
    coord: Coord
    edge_side: EdgeSide


@dataclass(frozen=True)
class Region:
    letter: str
    coords: FrozenSet[Coord]
    edges: FrozenSet[Edge]

    @property
    def area(self) -> int:
        return len(self.coords)

    @property
    def perimeter(self) -> int:
        return len(self.edges)

    def calculate_num_sides(self) -> int:
        num_sides = 0

        for side, coord_index in [
            (EdgeSide.LEFT, X),
            (EdgeSide.RIGHT, X),
            (EdgeSide.TOP, Y),
            (EdgeSide.BOTTOM, Y),
        ]:
            edges = [edge for edge in self.edges if edge.edge_side == side]
            grouped_edges = defaultdict(set)

            for edge in edges:
                key = edge.coord[coord_index]
                grouped_edges[key].add(edge.coord[1 - coord_index])

            num_sides += sum(
                self.get_num_contiguous_groups(sorted(coords))
                for coords in grouped_edges.values()
            )

        return num_sides

    @classmethod
    def get_num_contiguous_groups(cls, numbers: list[int]) -> int:
        if len(numbers) == 0:
            return 0

        sorted_numbers = sorted(numbers)
        return (
            sum(
                curr - prev != 1
                for prev, curr in zip(sorted_numbers, sorted_numbers[1:])
            )
            + 1
        )


def calculate_region_coords_and_edges(
    coord: Coord, farm_map: list[str], letter: str, coords: set[Coord], edges: set[Edge]
) -> None:
    if coord in coords:
        return

    coords.add(coord)

    x, y = coord
    for edge in [
        Edge((x + 1, y), EdgeSide.LEFT),
        Edge((x - 1, y), EdgeSide.RIGHT),
        Edge((x, y + 1), EdgeSide.TOP),
        Edge((x, y - 1), EdgeSide.BOTTOM),
    ]:
        dx, dy = edge.coord
        if (
            not (0 <= dx < len(farm_map[0]) and 0 <= dy < len(farm_map))
            or farm_map[dy][dx] != letter
        ):
            edges.add(edge)
            continue

        calculate_region_coords_and_edges((dx, dy), farm_map, letter, coords, edges)


def get_region(
    coord: Coord, farm_map: list[str], coord_to_region: dict[Coord, Region]
) -> Region:
    if coord in coord_to_region:
        return coord_to_region[coord]

    x, y = coord
    letter = farm_map[y][x]
    coords: set[Coord] = set()
    edges: set[Edge] = set()
    calculate_region_coords_and_edges(coord, farm_map, letter, coords, edges)

    region = Region(letter, frozenset(coords), frozenset(edges))

    for coord in coords:
        coord_to_region[coord] = region

    return region


def main() -> None:
    farm_map = Path("input/input.txt").read_text("utf-8").strip().split("\n")
    regions = set()
    coord_to_region: dict[Coord, Region] = dict()
    height = len(farm_map)
    width = len(farm_map[0])

    for x in range(width):
        for y in range(height):
            regions.add(get_region((x, y), farm_map, coord_to_region))

    print(sum(region.area * region.perimeter for region in regions))
    print(sum(region.area * region.calculate_num_sides() for region in regions))


if __name__ == "__main__":
    main()
