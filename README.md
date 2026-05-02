# cte-applicant-scoring

> A reusable AI skill for Baltimore Homecoming's Crab Tank Entrepreneurs program.

**Video walkthrough:** [ADD YOUR LINK HERE]

---

## What This Skill Does

This skill helps the Baltimore Homecoming selection committee evaluate Crab Tank
Entrepreneurs (CTE) applicants consistently and efficiently. It combines:

- **Hard eligibility filtering** — automatically flags applicants who don't meet
  program requirements before any scores are calculated
- **Weighted rubric scoring** — calculates a total score out of 50 across 10
  evaluation dimensions
- **Automatic ranking and categorization** — places every eligible applicant into
  a committee-ready tier (Definite / Maybe / Low Priority)
- **Actionable output** — surfaces top strengths, biggest gaps, and a recommended
  next step for each applicant

---

## Why I Built This

As Strategic Partnerships Manager at Baltimore Homecoming, I help run the
selection process for Crab Tank Entrepreneurs — a competitive grant program that
awards a $25,000 grand prize to Baltimore-based businesses.

Each cycle, committee members review 10+ applications individually and score each
one across 10 rubric dimensions. This process is time-consuming and can be
inconsistent across reviewers.

This skill solves that by giving the committee a reliable, consistent first pass —
so human reviewers can focus their energy on borderline cases and final
deliberation rather than reading every application from scratch.

The script is genuinely load-bearing here: a language model alone cannot
reliably apply weighted math across a spreadsheet of applicants, sort them,
check eligibility rules, and produce a clean ranked output. The script handles
all of that deterministically; Claude then interprets and summarizes the results.

---

## How to Use It

### Run the scorer
```bash
python .agents/skills/cte-applicant-scoring/scripts/score.py \
  path/to/applicants.csv \
  path/to/output.csv
```

### Input CSV format
Your CSV must include these columns:

**Eligibility columns** (yes / no):
- `baltimore_city_based`
- `revenue_generating`
- `has_supporting_team`
- `actively_operating`
- `scalable`
- `can_commit`
- `application_complete`

**Rubric columns** (integer 1–5):
- `problem_clarity`
- `solution_strength`
- `market_opportunity`
- `business_model`
- `traction_validation`
- `scalability`
- `baltimore_impact`
- `founder_team_strength`
- `execution_readiness`
- `commitment_engagement`

---

## What the Script Does

`scripts/score.py` handles all deterministic work:

1. Reads the input CSV row by row
2. Checks each applicant against 7 hard eligibility rules
3. Sums the 10 rubric dimension scores (1–5 each) for a total out of 50
4. Assigns a review category based on score thresholds
5. Identifies top 3 strengths and bottom 3 gaps per applicant
6. Generates a recommended next step
7. Sorts output: eligible applicants ranked by score, flagged applicants last
8. Writes a clean output CSV and prints a formatted summary to stdout

---

## Limitations

- The script scores based on pre-entered rubric values — it does not read raw application text
- All results require human review — this is a first-pass triage tool only
- Borderline cases must always go to committee

---

## Disclaimer

> AI scores are for committee reference only. All selections require human
> review and final committee approval.

---

## Folder Structure

```
hw5-Robinson/
├── .agents/
│   └── skills/
│       └── cte-applicant-scoring/
│           ├── SKILL.md
│           ├── scripts/
│           │   └── score.py
│           └── references/
│               ├── sample_applicants.csv
│               └── demo_prompts.md
└── README.md
```
