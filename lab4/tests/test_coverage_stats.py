from lab4.scripts.coverage_stats import parse_coverage_lines


def test_parse_coverage_lines_median() -> None:
    lines = [
        "20\t100\t200\t100",  # 100.0
        "20\t200\t300\t50",   # 50.0
        "20\t300\t400\t200",  # 200.0
    ]
    assert parse_coverage_lines(lines) == 100.0

