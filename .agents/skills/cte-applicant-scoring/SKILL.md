---
name: cte-applicant-scoring
description: Scores and ranks Crab Tank Entrepreneurs applicants using Baltimore Homecoming's eligibility filters and 50-point rubric. Use when reviewing structured applicant data, flagging disqualifiers, calculating scores, and preparing committee-ready candidate categories.
---

# CTE Applicant Scoring Skill

## When to Use This Skill
Use this skill when:
- A user provides a CSV of Crab Tank Entrepreneurs applicants to evaluate
- A user asks to rank, score, or filter CTE applicants
- A user wants to identify disqualified applicants before committee review
- A user asks for a committee-ready summary of the applicant pool

## When NOT to Use This Skill
- Do not use for final selection decisions — this is a first-pass triage tool only
- Do not use if the applicant data is incomplete or missing rubric scores
- Do not use for Homecoming Heroes applicants (different rubric)
- Do not make hiring or grant decisions based solely on this output

## Expected Inputs
A CSV file with the following columns:

applicant_name, business_name, baltimore_city_based, revenue_generating,
has_supporting_team, actively_operating, scalable, can_commit,
application_complete, problem_clarity, solution_strength,
market_opportunity, business_model, traction_validation, scalability,
baltimore_impact, founder_team_strength, execution_readiness,
commitment_engagement

- Eligibility columns should be yes or no
- Rubric columns should be integers 1–5

## Step-by-Step Instructions

1. Receive the CSV from the user (file path or pasted content)
2. Run the scoring script:
   python scripts/score.py <path-to-input.csv> <path-to-output.csv>
3. Read the output CSV — it contains each applicant's:
   - Eligibility status and disqualifier flags
   - Total score out of 50
   - Review category (Definite / Maybe / Low Priority / Flagged)
   - Top strengths and biggest gaps
4. Write a short committee summary covering:
   - Total applicants reviewed
   - How many are eligible vs. flagged
   - Top 3 candidates with brief rationale
   - Any patterns or concerns across the pool

## Hard Eligibility Disqualifiers
An applicant is automatically flagged if ANY of the following are true:
- baltimore_city_based = no → Not headquartered in Baltimore City
- revenue_generating = no → No paying customers or meaningful traction
- has_supporting_team = no → Running completely alone with no team/advisors
- actively_operating = no → Founder not actively running the business
- scalable = no → No realistic path to growth beyond lifestyle business
- can_commit = no → Cannot attend required events or meet deadlines
- application_complete = no → Missing pitch deck or required information

## Scoring Rubric (10 dimensions, 1–5 each = 50 points total)

1. Problem Clarity — How clearly the problem is defined
2. Solution Strength — How strong, realistic, and differentiated the solution is
3. Market Opportunity — Customer definition and market size
4. Business Model — Clear path to revenue and scalability
5. Traction & Validation — Proof of demand (revenue, users, pilots, partners)
6. Scalability — Growth potential beyond local/small operation
7. Baltimore Impact — Jobs, investment, community value in Baltimore
8. Founder & Team Strength — Experience, capacity, and support structure
9. Execution Readiness — Organization and readiness to move forward
10. Commitment & Engagement — Likelihood of full program participation

## Review Categories

- Definite (40–50): Strong fit, ready for committee review
- Maybe (30–39): Worth discussing, may need clarification
- Low Priority (20–29): Significant gaps, not competitive this cycle
- Flagged (Any): Failed at least one hard eligibility rule

## Expected Output Format
The script produces a ranked CSV. You should then provide:
1. A one-paragraph pool summary for the committee
2. A ranked table of eligible applicants with scores and categories
3. A separate list of flagged applicants with specific disqualifier reasons
4. A recommended next step for each top candidate

## Important Limitations
- AI scores are for committee reference only — all selections require human review
- Borderline cases must be reviewed by a human committee member
- The script cannot assess tone, body language, or verified track records
- Always display: "AI scores are for committee reference only. All selections require human review and final committee approval."
