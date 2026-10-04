def build_narrative(
    category,
    previous_revenue,
    current_revenue,
    mom_pct,
    month,
    prev_month
):
    return (
        f"### Context\n"
        f"{category} revenue changed from {previous_revenue} in "
        f"{prev_month} to {current_revenue} in {month}.\n\n"
        f"### Insight — Fact\n"
        f"{category} revenue changed by {mom_pct}% from "
        f"{prev_month} to {month}.\n\n"
        f"### Implication — Hypothesis\n"
        f"Review {category} performance between {prev_month} and {month} "
        f"to identify possible factors contributing to the observed change."
    )
