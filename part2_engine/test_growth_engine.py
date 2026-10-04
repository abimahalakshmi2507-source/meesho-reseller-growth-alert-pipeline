from growth_engine import mom_growth, is_flagged


def test_ethnic_wear():
    growth = mom_growth(104520.77, 185107.61)

    assert growth == 77.1
    assert is_flagged(growth) == "flagged"


def test_beauty_personal_care():
    growth = mom_growth(35542.11, 37559.07)

    assert growth == 5.67
    assert is_flagged(growth) == "not_flagged"


def test_exact_boundary():
    growth = mom_growth(100000, 108000)

    assert growth == 8.0
    assert is_flagged(growth) == "escalate_exact_boundary"

def test_corrupted_feed():
    from pathlib import Path
    import csv
    from growth_engine import validate_feed

    csv_path = Path(__file__).parent / "fixtures" / "corrupted_feed.csv"

    with open(csv_path, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    valid, errors = validate_feed(rows)

    negative_line, negative_row = next(
        (line, row)
        for line, row in enumerate(rows, start=2)
        if float(row["revenue"]) < 0
    )
    missing_category_line, missing_category_row = next(
        (line, row)
        for line, row in enumerate(rows, start=2)
        if not row["category"].strip()
    )
    missing_revenue_line, missing_revenue_row = next(
        (line, row)
        for line, row in enumerate(rows, start=2)
        if not row["revenue"].strip()
    )
    expected_errors = [
        f"line {negative_line}: negative revenue ({float(negative_row['revenue'])}) "
        f"for category={negative_row['category']}",
        f"line {missing_category_line}: missing category "
        f"(month={missing_category_row['month']})",
        f"line {missing_revenue_line}: missing revenue "
        f"(category={missing_revenue_row['category']})",
    ]

    assert valid is False
    assert errors == expected_errors
