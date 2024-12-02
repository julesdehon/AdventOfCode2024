from collections import defaultdict
from pathlib import Path


def main() -> None:
    input_lines = Path("input/input.txt").read_text("utf-8").split("\n")
    n1s, n2s = zip(*[
        (int(n1), int(n2))
        for n1, n2 in [line.split(maxsplit=2) for line in input_lines if line != ""]
    ])
    sorted_n1s, sorted_n2s = sorted(n1s), sorted(n2s)

    distances = [abs(n1 - n2) for n1, n2 in zip(sorted_n1s, sorted_n2s)]
    print(f"The total distance between the two lists is {sum(distances)}")

    n2_frequencies: dict[int, int] = defaultdict(int)
    for n2 in sorted_n2s:
        n2_frequencies[n2] += 1

    similarity_scores = [n1 * n2_frequencies[n1] for n1 in sorted_n1s]
    print(f"The similarity score is {sum(similarity_scores)}")


if __name__ == "__main__":
    main()
