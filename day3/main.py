import re
from pathlib import Path

MUL_REGEX = r"mul\((\d{1,3}),(\d{1,3})\)"
MUL_AND_CONDITIONALS_REGEX = rf"({MUL_REGEX})|(do\(\))|(don't\(\))"


def main() -> None:
    input_text = Path("input/input.txt").read_text("utf-8")

    total = 0
    for match in re.finditer(MUL_REGEX, input_text):
        x = int(match.group(1))
        y = int(match.group(2))
        total += x * y

    print(f"If you add up all the multiplications you get {total}")

    enabled = True
    total_with_conditionals = 0
    for match in re.finditer(MUL_AND_CONDITIONALS_REGEX, input_text):
        if match.group(4):
            enabled = True
            continue

        if match.group(5):
            enabled = False
            continue

        if enabled:
            x = int(match.group(2))
            y = int(match.group(3))
            total_with_conditionals += x * y

    print(
        "When accounting for conditional statements, if you add up all the"
        f" multiplications you get {total_with_conditionals}"
    )


if __name__ == "__main__":
    main()
