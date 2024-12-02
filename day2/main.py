from pathlib import Path


def is_safe(report: list[int]) -> bool:
    is_sorted = report == sorted(report) or report == sorted(report, reverse=True)

    differences = [abs(x - y) for x, y in zip(report[1:], report[:-1])]
    are_differences_safe = all(1 <= diff <= 3 for diff in differences)

    return is_sorted and are_differences_safe


def is_safe_with_dampener(report: list[int]) -> bool:
    sub_reports = [report[:i] + report[i + 1 :] for i in range(len(report))]

    return any(is_safe(sub_report) for sub_report in sub_reports)


def main() -> None:
    input_lines = Path("input/input.txt").read_text("utf-8").split("\n")
    reports = [[int(n) for n in line.split()] for line in input_lines if line != ""]
    safe_reports = [report for report in reports if is_safe(report)]
    print(f"There were {len(safe_reports)} safe reports")

    safe_reports_with_dampener = [
        report for report in reports if is_safe_with_dampener(report)
    ]
    print(
        "Accounting for the problem dampener, there are"
        f" {len(safe_reports_with_dampener)} safe reports"
    )


if __name__ == "__main__":
    main()
