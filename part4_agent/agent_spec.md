# Part 4 — Agent Specification

## Purpose

The agent validates the current-month reseller revenue feed, calculates month-over-month growth, identifies flagged categories, and prepares stakeholder-ready draft messages for approval.

## Inputs

- Run month
- Previous-month CSV
- Current-month CSV

## Workflow

1. Validate the current-month feed.
2. If validation fails, stop the run.
3. Calculate MoM growth for every category.
4. Apply the Part 2 is_flagged() function.
5. Sort flagged categories by absolute MoM percentage in descending order.
6. Draft messages for at most the top 3 flagged categories.
7. Mark remaining flagged categories as suppressed, review manually.
8. Record exact-boundary cases separately.
9. Return structured JSON.

## Guardrails

- Reuse the Part 2 growth functions without modification.
- Do not send messages automatically.
- Do not call external APIs.
- Do not use API keys.
- Do not invent causes for revenue changes.
- Use the Part 3 prompt-pack logic for narrative drafts.
- If validation fails, do not calculate or draft MoM alerts.

## Output

The agent returns:

- run_month
- validation_status
- validation_errors
- flagged_categories
- suppressed_categories
- escalated_categories
- action_taken

## Actions

If the feed is valid:

drafted_and_held_for_approval

If the feed is invalid:

hard_stop
