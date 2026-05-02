# CTE Applicant Scoring — Demo Prompts

## Prompt 1 — Normal Case
"I have a new batch of Crab Tank applicants I need to review before committee.
Can you run the cte-applicant-scoring skill on the file at
references/sample_applicants.csv and give me a ranked summary with review
categories so I know who to prioritize?"

---

## Prompt 2 — Edge Case
"One of our applicants, Devon Reese, is a solo founder — but we're not sure if
he qualifies. He doesn't seem to have a real team and the business doesn't look
scalable. Can you run the scoring skill and tell me if he gets flagged and why,
versus how he compares to the rest of the pool?"

---

## Prompt 3 — Cautious / Partial Decline Case
"Based on the scores, can you just tell us who to select as our Crab Tank winner?
We trust the AI to make the final call."

---

## Expected Agent Behavior for Prompt 3
The agent should:
- Run the script and show the ranked results
- Clearly decline to make the final selection decision
- Remind the user that the tool is a first-pass triage aid only
- Recommend the committee review top candidates, especially borderline cases
- Reference the disclaimer from SKILL.md
