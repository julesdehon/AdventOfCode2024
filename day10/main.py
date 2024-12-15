from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Generic, Type, TypeVar

Coord = tuple[int, int]
T = TypeVar("T", bound="ITrailMeasure")


class ITrailMeasure(ABC, Generic[T]):
    @staticmethod
    @abstractmethod
    def zero() -> T:
        pass

    @staticmethod
    @abstractmethod
    def one(coord: Coord) -> T:
        pass

    @abstractmethod
    def combine(self, measure: T) -> T:
        pass

    @abstractmethod
    def get(self) -> int:
        pass


@dataclass
class Score(ITrailMeasure["Score"]):
    reachable_9s: set

    @staticmethod
    def zero() -> "Score":
        return Score(set())

    @staticmethod
    def one(coord: Coord) -> "Score":
        return Score({coord})

    def combine(self, score: "Score") -> "Score":
        return Score(self.reachable_9s.union(score.reachable_9s))

    def get(self) -> int:
        return len(self.reachable_9s)


@dataclass
class Rating(ITrailMeasure["Rating"]):
    rating: int

    @staticmethod
    def zero() -> "Rating":
        return Rating(0)

    @staticmethod
    def one(coord: Coord) -> "Rating":
        return Rating(1)

    def combine(self, rating: "Rating") -> "Rating":
        return Rating(self.rating + rating.rating)

    def get(self) -> int:
        return self.rating


def get_measure(
    coord: Coord,
    topological_map: list[list[int]],
    measure_cache: dict[Coord, T],
    measure_cls: Type[T],
) -> T:
    x, y = coord
    if (x, y) in measure_cache:
        return measure_cache[(x, y)]

    val = topological_map[y][x]
    if val == 9:
        return measure_cls.one(coord)

    measure = measure_cls.zero()
    for dx, dy in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
        if not (0 <= dx < len(topological_map[0]) and 0 <= dy < len(topological_map)):
            continue

        if val + 1 == topological_map[dy][dx]:
            measure = measure.combine(
                get_measure((dx, dy), topological_map, measure_cache, measure_cls)
            )

    return measure


def calculate_sum_of_measures(
    topological_map: list[list[int]], measure_cls: Type[T]
) -> int:
    coord_to_measure: dict[Coord, T] = dict()
    for y in range(len(topological_map)):
        for x in range(len(topological_map)):
            coord_to_measure[(x, y)] = get_measure(
                (x, y), topological_map, coord_to_measure, measure_cls
            )

    return sum(
        score.get()
        for (x, y), score in coord_to_measure.items()
        if topological_map[y][x] == 0
    )


def main() -> None:
    topological_map = [
        [int(val) for val in row]
        for row in Path("input/input.txt").read_text("utf-8").strip().split("\n")
    ]

    print(calculate_sum_of_measures(topological_map, Score))
    print(calculate_sum_of_measures(topological_map, Rating))


if __name__ == "__main__":
    main()
