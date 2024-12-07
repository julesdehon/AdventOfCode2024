from collections import defaultdict
from dataclasses import dataclass
from functools import cmp_to_key
from pathlib import Path


@dataclass
class Rule:
    comes_first: int
    comes_second: int

    @staticmethod
    def from_str(raw_rule: str) -> "Rule":
        comes_first, comes_second = raw_rule.split("|", maxsplit=2)

        return Rule(int(comes_first), int(comes_second))


@dataclass
class Comparer:
    _comes_first_to_all_that_come_second: dict[int, set[int]]

    @staticmethod
    def from_rules(rules: list[Rule]) -> "Comparer":
        comes_first_to_all_that_come_second = defaultdict(set)
        for rule in rules:
            comes_first_to_all_that_come_second[rule.comes_first].add(rule.comes_second)

        return Comparer(comes_first_to_all_that_come_second)

    def compare(self, a: int, b: int) -> int:
        if b in self._comes_first_to_all_that_come_second[a]:
            return -1

        if a in self._comes_first_to_all_that_come_second[b]:
            return 1

        return 0


def main() -> None:
    raw_rules, raw_updates = Path("input/input.txt").read_text("utf-8").split("\n\n")

    rules = [Rule.from_str(raw_rule) for raw_rule in raw_rules.split("\n")]
    updates = [
        [int(x) for x in raw_update.split(",")]
        for raw_update in raw_updates.split("\n")
        if raw_update != ""
    ]

    comparer = Comparer.from_rules(rules)
    sorted_updates = [
        sorted(update, key=cmp_to_key(comparer.compare)) for update in updates
    ]

    correctly_ordered_updates = [
        update
        for update, sorted_update in zip(updates, sorted_updates)
        if update == sorted_update
    ]
    sum_of_correctly_ordered_middles = sum(
        update[len(update) // 2] for update in correctly_ordered_updates
    )
    print(
        "If you add up the middle page number from all correctly-ordered updates, you"
        f" get {sum_of_correctly_ordered_middles}"
    )

    sorted_version_of_incorrectly_ordered_updates = [
        sorted_update
        for update, sorted_update in zip(updates, sorted_updates)
        if update != sorted_update
    ]
    sum_of_sorted_version_of_incorrectly_ordered_middles = sum(
        update[len(update) // 2]
        for update in sorted_version_of_incorrectly_ordered_updates
    )
    print(
        "If you add up the middle page number from the sorted version of the"
        " incorrectly-ordered updates, you get"
        f" {sum_of_sorted_version_of_incorrectly_ordered_middles}"
    )


if __name__ == "__main__":
    main()
