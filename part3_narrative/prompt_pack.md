# Reusable Prompt Pack

## Trigger

Run this prompt when a category's is_flagged result is "flagged".

## Input List

- {category} — category name
- {previous_revenue} — revenue in the previous month
- {current_revenue} — revenue in the current month
- {mom_pct} — month-over-month growth percentage
- {month} — current month
- {prev_month} — previous month

## Prompt

You are writing a concise stakeholder update for a regional manager.

Use the following supplied values only:

- Category: [{category}]
- Previous month: [{prev_month}]
- Current month: [{month}]
- Previous revenue: [{previous_revenue}]
- Current revenue: [{current_revenue}]
- MoM change: [{mom_pct}]%

Write the update using this structure:

### Context
State the category and the supplied revenue figures for [{prev_month}] and [{month}].

### Insight
Explain the month-over-month change using [{mom_pct}]%.

### Implication
Give one specific and actionable recommendation based only on the supplied information.

Do not invent, estimate, or calculate any additional numbers.
Never state a number that is not one of the supplied placeholder values.
Clearly distinguish facts from hypotheses.
Do not identify any reseller by a real name; use only a coded alias if a reseller is provided.

## Checklist

Before using the output, verify:

1. Every number in the draft matches a supplied placeholder value exactly.
2. The Context → Insight → Implication structure is present.
3. Facts and hypotheses are clearly distinguished.
4. The recommendation is specific and actionable.
5. No real reseller name or other internal identifier is exposed.
6. No unsupported claim or invented information has been added.
