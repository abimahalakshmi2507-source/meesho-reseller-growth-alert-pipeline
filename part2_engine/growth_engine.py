import csv
from pathlib import Path

def mom_growth(previous, current):
    if previous == 0:
        return None

    return round((current - previous) / previous * 100, 2)

def is_flagged(mom_pct, threshold=8.0):
    if abs(mom_pct) > threshold:
        return "flagged"

    if abs(mom_pct) < threshold:
        return "not_flagged"

    return "escalate_exact_boundary"

def validate_feed(rows):
    errors = []

    for line_number, row in enumerate(rows, start=2):
        month = row.get("month", "")
        category = row.get("category", "")
        revenue = row.get("revenue", "")

        if not category.strip():
            errors.append(
                f"line {line_number}: missing category (month={month})"
            )

        if revenue.strip() == "":
            errors.append(
                f"line {line_number}: missing revenue (category={category})"
            )
        else:
            try:
                revenue_value = float(revenue)
            except ValueError:
                errors.append(
                    f"line {line_number}: revenue not numeric: {revenue!r}"
                )
            else:
                if revenue_value < 0:
                    errors.append(
                        f"line {line_number}: negative revenue ({revenue_value}) "
                        f"for category={category}"
                    )

    return (True, []) if not errors else (False, errors)



BASE_DIR = Path(__file__).resolve().parent.parent

csv_file = BASE_DIR / "part1_sql" / "output" / "monthly_category_revenue.csv"
with open(csv_file, "r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

print(f"Loaded {len(rows)} rows")

errors = validate_feed(rows)

print("Validation errors:", errors)
if errors[0] is False:
    print("Feed invalid. Stopping.")
    raise SystemExit
growth_results = []

for category in sorted(set(row["category"] for row in rows)):
    category_rows = [row for row in rows if row["category"] == category]

    april = next(row for row in category_rows if row["month"] == "April")
    may = next(row for row in category_rows if row["month"] == "May")
    june = next(row for row in category_rows if row["month"] == "June")

    april_may_growth = mom_growth(
        float(april["revenue"]),
        float(may["revenue"])
    )

    may_june_growth = mom_growth(
        float(may["revenue"]),
        float(june["revenue"])
    )

    growth_results.append({
        "category": category,
        "April_to_May": april_may_growth,
        "May_to_June": may_june_growth
    })
