from pathlib import Path
import csv
import sys

# Part 2 imports
sys.path.append(
    str(Path(__file__).resolve().parent.parent / "part2_engine")
)

from growth_engine import mom_growth, is_flagged, validate_feed

# Part 3 imports
sys.path.append(
    str(Path(__file__).resolve().parent.parent / "part3_narrative")
)

from narrative_engine import build_narrative

def load_csv(csv_path):
    with open(csv_path, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def run(month, previous_month_csv, current_month_csv):

    previous_rows = load_csv(previous_month_csv)
    current_rows = load_csv(current_month_csv)

    # Validate current-month feed
    valid, errors = validate_feed(current_rows)

    if not valid:
        return {
            "run_month": month,
            "validation_status": "invalid",
            "validation_errors": errors,
            "flagged_categories": [],
            "suppressed_categories": [],
            "escalated_categories": [],
            "action_taken": "hard_stop"
        }

    # Identify previous month
    month_map = {
        "May": "April",
        "June": "May"
    }

    previous_month = month_map[month]

    # Filter required months
    previous_rows = [
        row for row in previous_rows
        if row["month"] == previous_month
    ]

    current_rows = [
        row for row in current_rows
        if row["month"] == month
    ]

    # Get categories
    categories = sorted(
        set(row["category"] for row in current_rows)
    )

    results = []

    # Calculate MoM for every category
    for category in categories:

        previous = next(
            row for row in previous_rows
            if row["category"] == category
        )

        current = next(
            row for row in current_rows
            if row["category"] == category
        )

        mom_pct = mom_growth(
            float(previous["revenue"]),
            float(current["revenue"])
        )

        status = is_flagged(mom_pct)

        results.append({
            "category": category,
            "mom_pct": mom_pct,
            "previous_revenue": float(previous["revenue"]),
            "current_revenue": float(current["revenue"]),
            "status": status
        })

    # Separate flagged and exact-boundary categories
    flagged = [
        row for row in results
        if row["status"] == "flagged"
    ]

    escalated = [
        row for row in results
        if row["status"] == "escalate_exact_boundary"
    ]

    # Sort flagged categories by absolute MoM
    flagged.sort(
        key=lambda row: abs(row["mom_pct"]),
        reverse=True
    )

    # Top 3 are drafted
    top_three = flagged[:3]

    # Remaining flagged categories are suppressed
    suppressed = flagged[3:]

    drafted_categories = []

    for row in top_three:

        message = build_narrative(
            category=row["category"],
            previous_revenue=row["previous_revenue"],
            current_revenue=row["current_revenue"],
            mom_pct=row["mom_pct"],
            month=month,
            prev_month=previous_month
        )

        drafted_categories.append({
            "category": row["category"],
            "mom_pct": row["mom_pct"],
            "previous_revenue": row["previous_revenue"],
            "current_revenue": row["current_revenue"],
            "drafted": True,
            "message": message
        })

    suppressed_categories = [
        {
            "category": row["category"],
            "mom_pct": row["mom_pct"],
            "status": "suppressed, review manually"
        }
        for row in suppressed
    ]

    escalated_categories = [
        {
            "category": row["category"],
            "mom_pct": row["mom_pct"]
        }
        for row in escalated
    ]

    return {
        "run_month": month,
        "validation_status": "valid",
        "validation_errors": [],
        "flagged_categories": drafted_categories,
        "suppressed_categories": suppressed_categories,
        "escalated_categories": escalated_categories,
        "action_taken": "drafted_and_held_for_approval"
    }


if __name__ == "__main__":

    base_dir = Path(__file__).resolve().parent.parent

    previous_csv = (
        base_dir
        / "part1_sql"
        / "output"
        / "monthly_category_revenue.csv"
    )

    current_csv = (
        base_dir
        / "part1_sql"
        / "output"
        / "monthly_category_revenue.csv"
    )

    result = run(
        "May",
        str(previous_csv),
        str(current_csv)
    )

    print(result)
