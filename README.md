# Meesho Reseller Growth & Alert Intelligence Pipeline

## Project Overview

This project analyzes reseller revenue data and identifies important month-over-month (MoM) changes.

The pipeline connects:

*SQL → Python Growth Engine → Narrative Logic → Mock Agent*

The project works offline and does not require API keys.

## Project Structure

```text
Meesho/
├── data/
├── part1_sql/
├── part2_engine/
├── part3_narrative/
├── part4_agent/
└── README.md 


## Part 1 — SQL Analysis

Part 1 uses the generated reseller dataset and SQL queries to produce:
- Monthly category revenue
- Region revenue
- Top resellers
- Zero-order reseller checks
- June delivered-order AOV
Run:
   python part1_sql/run_queries.py

The results are saved inside:
   part1_sql/output/


## Part 2 — Growth Engine

The growth engine:

- Validates the revenue feed.
- Calculates MoM growth.
- Applies the 8% flagging threshold.
- Tests corrupted input.

Run the tests:
   cd part2_engine
   python -m pytest test_growth_engine.py

Expected result:
    4 passed


## Part 3 — Narrative & Masking

Part 3 contains:

- Reusable prompt pack
- Stakeholder narrative examples
- Chart-choice justification
- Reseller-name masking

Important files:

part3_narrative
├── prompt_pack.md
├── narrative_report.md
├── narrative_engine.py
└── masking.py

## Part 4 — Mock Agent

The mock agent:

- Validates the current feed.
- Stops if validation fails.
- Calculates MoM growth.
- Identifies flagged categories.
- Drafts messages for the top 3 flagged categories.
- Suppresses remaining flagged categories.
- Records exact-boundary cases.
- Holds drafts for approval instead of sending them.

Important files:
part4_agent/
├── agent_spec.md
└── mock_agent_runner.py

Run:
 python part4_agent/mock_agent_runner.py

## Guardrails:
- No external API calls
- No API keys required
- No automatic message sending
- Invalid feeds cause a hard stop
- Part 2 growth functions are reused without modification
- Narrative causes are not presented as confirmed facts
- Reseller names are masked in the narrative


## Test Coverage

The project verifies:

- May: April → May MoM alerts
- June: May → June MoM alerts
- Exact 8% boundary behavior
- Corrupted-feed validation
- Hard-stop behavior for invalid data
- Reseller-name masking

## Dataset
The dataset is generated locally using the provided dataset generation script.

Run:
python data/generate_dataset.py

The generated data is stored in the data/ folder.

## How the Parts Connect

1. Part 1 uses SQL to analyze the reseller dataset and generate CSV outputs.
2. Part 2 validates the monthly revenue feed and calculates MoM growth and flag status.
3. Part 3 provides the narrative prompt logic, stakeholder narratives, chart choices, and reseller-name masking.
4. Part 4 reuses the Part 2 growth engine and applies the narrative logic to draft alerts.
5. Invalid data causes a hard stop, and valid alert drafts are held for approval instead of being sent automatically.

