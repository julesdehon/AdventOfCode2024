import math
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

Vector = tuple[int, int]


WIDTH = 101
HEIGHT = 103


@dataclass
class Robot:
    position: Vector
    velocity: Vector

    @staticmethod
    def from_str(raw_robot: str) -> "Robot":
        raw_p, raw_v = raw_robot.split(" ", maxsplit=2)
        px, py = [int(n) for n in raw_p[2:].split(",", maxsplit=2)]
        vx, vy = [int(n) for n in raw_v[2:].split(",", maxsplit=2)]

        return Robot((px, py), (vx, vy))

    def step(self) -> None:
        (px, py), (vx, vy) = self.position, self.velocity
        px2, py2 = (px + vx), (py + vy)

        self.position = self._wrap((px2, py2))

    def quadrant(self) -> Optional[int]:
        x, y = self.position
        mid_x = WIDTH // 2
        mid_y = HEIGHT // 2

        if x == mid_x or y == mid_y:
            return None

        qx = 0 if x < mid_x else 1
        qy = 0 if y < mid_y else 1

        return 2 * qx + qy

    @classmethod
    def _wrap(cls, position: Vector) -> Vector:
        x, y = position
        if x < 0:
            x = WIDTH + x

        if y < 0:
            y = HEIGHT + y

        return x % WIDTH, y % HEIGHT


def safety_factor(robots: list[Robot]) -> int:
    quadrant_to_count: dict[int, int] = defaultdict(int)
    for robot in robots:
        maybe_quadrant = robot.quadrant()
        if maybe_quadrant is not None:
            quadrant_to_count[maybe_quadrant] += 1

    return math.prod(quadrant_to_count.values())


def get_map(robots: list[Robot]) -> str:
    coord_to_count: dict[Vector, int] = defaultdict(int)
    for robot in robots:
        coord_to_count[robot.position] += 1

    robot_map = ""
    for y in range(HEIGHT):
        s = ""
        for x in range(WIDTH):
            s += str(coord_to_count[(x, y)]) if (x, y) in coord_to_count else "."
        robot_map += f"{s}\n"

    return robot_map


def main() -> None:
    input_lines = Path("input/input.txt").read_text("utf-8").strip().split("\n")
    robots = [Robot.from_str(raw_robot) for raw_robot in input_lines]

    for i in range(100):
        for robot in robots:
            robot.step()

    print(safety_factor(robots))

    robots = [Robot.from_str(raw_robot) for raw_robot in input_lines]
    for i in range(100_000_000):
        coord_to_count: dict[Vector, int] = defaultdict(int)
        for robot in robots:
            coord_to_count[robot.position] += 1

        robot_map = get_map(robots)
        if "111111" in robot_map:
            print(i)
            print(robot_map)

        for robot in robots:
            robot.step()


if __name__ == "__main__":
    main()
