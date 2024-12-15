from dataclasses import dataclass
from pathlib import Path

from utils.helpers import parse_value_between_strings

Vector = tuple[int, int]


@dataclass
class ClawMachine:
    prize: Vector
    a: Vector
    b: Vector

    @staticmethod
    def from_str(raw_machine: str, prize_offset: int = 0) -> "ClawMachine":
        raw_a, raw_b, raw_prize = raw_machine.split("\n", maxsplit=3)
        a_x = parse_value_between_strings(raw_a, "X+", ",", int)
        a_y = int(raw_a[raw_a.find("Y+") + len("Y+") :])
        b_x = parse_value_between_strings(raw_b, "X+", ",", int)
        b_y = int(raw_b[raw_b.find("Y+") + len("Y+") :])
        prize_x = prize_offset + parse_value_between_strings(raw_prize, "X=", ",", int)
        prize_y = prize_offset + int(raw_prize[raw_prize.find("Y=") + len("Y=") :])

        return ClawMachine((prize_x, prize_y), (a_x, a_y), (b_x, b_y))

    def get_price(self) -> int:
        (p1, p2), (a1, a2), (b1, b2) = self.prize, self.a, self.b
        y = (p2 * a1 - a2 * p1) / (b2 * a1 - a2 * b1)
        x = (p1 - y * b1) / a1

        if abs(x % 1 - 0) > 1e-6 or abs(y % 1 - 0) > 1e-6:
            return 0

        return 3 * int(x) + int(y)


def main() -> None:
    raw_machines = Path("input/input.txt").read_text("utf-8").strip().split("\n\n")

    claw_machines = [ClawMachine.from_str(raw_machine) for raw_machine in raw_machines]
    print(sum(claw_machine.get_price() for claw_machine in claw_machines))

    claw_machines_with_offset = [
        ClawMachine.from_str(raw_machine, prize_offset=10_000_000_000_000)
        for raw_machine in raw_machines
    ]
    print(sum(claw_machine.get_price() for claw_machine in claw_machines_with_offset))


if __name__ == "__main__":
    main()
