from dataclasses import dataclass
from enum import Enum
from pathlib import Path

Coord = tuple[int, int]


class Direction(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3


@dataclass
class Guard:
    position: Coord
    direction: Direction

    @staticmethod
    def create(position: Coord) -> "Guard":
        return Guard(position, Direction.UP)

    def get_next_position(self) -> Coord:
        (x, y) = self.position
        if self.direction == Direction.RIGHT:
            return x + 1, y
        elif self.direction == Direction.DOWN:
            return x, y + 1
        elif self.direction == Direction.LEFT:
            return x - 1, y
        elif self.direction == Direction.UP:
            return x, y - 1

        raise Exception("Unknown Direction")

    def move_forward(self) -> None:
        self.position = self.get_next_position()

    def turn_90_deg_right(self) -> None:
        if self.direction == Direction.RIGHT:
            self.direction = Direction.DOWN
        elif self.direction == Direction.DOWN:
            self.direction = Direction.LEFT
        elif self.direction == Direction.LEFT:
            self.direction = Direction.UP
        elif self.direction == Direction.UP:
            self.direction = Direction.RIGHT
        else:
            raise Exception("Unknown Direction")


@dataclass
class Map:
    width: int
    height: int
    obstacles: set[Coord]
    guard: Guard

    @staticmethod
    def from_str(map_str: str) -> "Map":
        obstacles = set()
        guard = None

        rows = map_str.split("\n")
        height = len(rows)
        width = len(rows[0])
        for y, row in enumerate(rows):
            for x in range(len(row)):
                if rows[y][x] == ".":
                    continue
                if rows[y][x] == "^":
                    guard = Guard.create((x, y))
                if rows[y][x] == "#":
                    obstacles.add((x, y))

        if guard is None:
            raise Exception("No guard found")

        return Map(width, height, obstacles, guard)

    def step(self) -> bool:
        if self.guard.get_next_position() in self.obstacles:
            self.guard.turn_90_deg_right()
        else:
            self.guard.move_forward()

        return self.is_in_map(self.guard.position)

    def is_in_map(self, coord: Coord) -> bool:
        x, y = coord
        return 0 <= x < self.width and 0 <= y < self.height


def main() -> None:
    map_str = Path("input/input.txt").read_text("utf-8").strip()
    area_map = Map.from_str(map_str)

    visited_positions = {area_map.guard.position}
    while area_map.step():
        visited_positions.add(area_map.guard.position)

    print(f"The guard visits {len(visited_positions)} unique positions")

    num_loops = 0
    for x, y in visited_positions:
        area_map = Map.from_str(map_str)
        if (x, y) == area_map.guard.position:
            continue

        area_map.obstacles.add((x, y))
        visited_positions_and_directions = {
            (area_map.guard.position, area_map.guard.direction)
        }
        while area_map.step():
            if (
                area_map.guard.position,
                area_map.guard.direction,
            ) in visited_positions_and_directions:
                num_loops += 1
                break

            visited_positions_and_directions.add(
                (area_map.guard.position, area_map.guard.direction)
            )

    print(f"{num_loops} obstructions positions result in a guard loop")


if __name__ == "__main__":
    main()
