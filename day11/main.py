from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Stone:
    num: int

    def blink(self) -> list["Stone"]:
        if self.num == 0:
            return [Stone(1)]

        num_str = str(self.num)
        num_digits = len(num_str)
        if num_digits % 2 == 0:
            left, right = num_str[: num_digits // 2], num_str[num_digits // 2 :]
            return [Stone(int(left)), Stone(int(right))]

        return [Stone(self.num * 2024)]


def get_number_of_stones_after_b_blinks(stones: list[Stone], n: int) -> int:
    stone_to_occurrences: dict[Stone, int] = defaultdict(int)
    for stone in stones:
        stone_to_occurrences[stone] += 1

    for i in range(n):
        new_stone_to_occurrences = stone_to_occurrences.copy()
        for stone, occurrences in stone_to_occurrences.items():
            new_stones = stone.blink()
            new_stone_to_occurrences[stone] -= occurrences
            for new_stone in new_stones:
                new_stone_to_occurrences[new_stone] += occurrences
        stone_to_occurrences = new_stone_to_occurrences

    return sum(occurrences for occurrences in stone_to_occurrences.values())


def main() -> None:
    stones = [
        Stone(int(num))
        for num in Path("input/input.txt").read_text("utf-8").strip().split(" ")
    ]

    print(get_number_of_stones_after_b_blinks(stones, 25))
    print(get_number_of_stones_after_b_blinks(stones, 75))


if __name__ == "__main__":
    main()
