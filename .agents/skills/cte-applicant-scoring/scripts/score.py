#!/usr/bin/env python3
"""
CTE Applicant Scorer
Baltimore Homecoming — Crab Tank Entrepreneurs Program

Usage:
    python score.py <input_csv> [output_csv]
"""

import csv
import sys
from pathlib import Path

RUBRIC_DIMS = [
    "problem_clarity",
    "solution_strength",
    "market_opportunity",
    "business_model",
    "traction_validation",
    "scalability",
    "baltimore_impact",
    "founder_team_strength",
    "execution_readiness",
    "commitment_engagement",
]

ELIGIBILITY_FIELDS = {
    "baltimore_city_based": "Not headquartered in Baltimore City",
    "revenue_generating":   "No paying customers or meaningful traction",
    "has_supporting_team":  "Running completely alone — no team, advisors, or support",
    "actively_operating":   "Founder not actively operating the business",
    "scalable":             "No realistic path to growth (lifestyle/hobby business)",
    "can_commit":           "Cannot attend required events or meet program deadlines",
    "application_complete": "Incomplete application — missing pitch deck or key info",
}

CATEGORY_THRESHOLDS = {
    "Definite":     (40, 50),
    "Maybe":        (30, 39),
    "Low Priority": (20, 29),
    "Weak Fit":     (0,  19),
}


def check_eligibility(row):
    flags = []
    for field, reason in ELIGIBILITY_FIELDS.items():
        val = row.get(field, "").strip().lower()
        if val == "no":
            flags.append(reason)
    return flags


def compute_score(row):
    total = 0
    warnings = []
    for dim in RUBRIC_DIMS:
        raw = row.get(dim, "").strip()
        if not raw:
            warnings.append(f"Missing value for '{dim}' — counted as 0")
            continue
        try:
            val = int(raw)
            if not (1 <= val <= 5):
                warnings.append(f"'{dim}' = {val} is out of range (1-5) — clamped")
                val = max(1, min(5, val))
            total += val
        except ValueError:
            warnings.append(f"'{dim}' = '{raw}' is not a number — counted as 0")
    return total, warnings


def assign_category(score, disqualifiers):
    if disqualifiers:
        return "Flagged"
    for category, (lo, hi) in CATEGORY_THRESHOLDS.items():
        if lo <= score <= hi:
            return category
    return "Weak Fit"


def top_strengths(row, n=3):
    scores = {}
    for dim in RUBRIC_DIMS:
        try:
            scores[dim] = int(row.get(dim, 0))
        except ValueError:
            scores[dim] = 0
    top = sorted(scores, key=scores.get, reverse=True)[:n]
    return ", ".join(d.replace("_", " ").title() for d in top)


def biggest_gaps(row, n=3):
    scores = {}
    for dim in RUBRIC_DIMS:
        try:
            scores[dim] = int(row.get(dim, 0))
        except ValueError:
            scores[dim] = 0
    bottom = sorted(scores, key=scores.get)[:n]
    return ", ".join(d.replace("_", " ").title() for d in bottom)


def recommended_next_step(category, disqualifiers):
    if disqualifiers:
        return "Do not advance. Flag for staff review before any communication."
    if category == "Definite":
        return "Advance to committee shortlist. Schedule for panel review."
    if category == "Maybe":
        return "Hold for committee discussion. Request clarification if needed."
    if category == "Low Priority":
        return "Do not advance this cycle. Consider for future programs."
    return "Do not advance. Significant gaps across multiple dimensions."


def score_applicants(input_path):
    results = []
    with open(input_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            disqualifiers = check_eligibility(row)
            total, warnings = compute_score(row)
            category = assign_category(total, disqualifiers)
            result = {
                "applicant_name":        row.get("applicant_name", "").strip(),
                "business_name":         row.get("business_name", "").strip(),
                "eligibility_status":    "Flagged" if disqualifiers else "Eligible",
                "disqualifier_flags":    " | ".join(disqualifiers) if disqualifiers else "None",
                "total_score":           total,
                "max_score":             50,
                "average_score":         round(total / len(RUBRIC_DIMS), 1),
                "review_category":       category,
                "top_strengths":         top_strengths(row),
                "biggest_gaps":          biggest_gaps(row),
                "recommended_next_step": recommended_next_step(category, disqualifiers),
                "data_warnings":         " | ".join(warnings) if warnings else "None",
            }
            results.append(result)
    results.sort(key=lambda r: (r["eligibility_status"] == "Flagged", -r["total_score"]))
    return results


def write_output(results, output_path):
    if not results:
        print("No results to write.")
        return
    fieldnames = list(results[0].keys())
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


def print_summary(results):
    eligible = [r for r in results if r["eligibility_status"] == "Eligible"]
    flagged  = [r for r in results if r["eligibility_status"] == "Flagged"]
    print("\n" + "=" * 60)
    print("  CTE APPLICANT SCORING REPORT")
    print("  Baltimore Homecoming — Crab Tank Entrepreneurs")
    print("=" * 60)
    print(f"\n  Total applicants reviewed : {len(results)}")
    print(f"  Eligible                  : {len(eligible)}")
    print(f"  Flagged / Disqualified    : {len(flagged)}")
    for cat in ["Definite", "Maybe", "Low Priority", "Weak Fit"]:
        count = sum(1 for r in eligible if r["review_category"] == cat)
        if count:
            print(f"    {cat:<18}: {count}")
    print("\n-- ELIGIBLE APPLICANTS (ranked) --")
    for r in eligible:
        print(f"\n  {r['applicant_name']} — {r['business_name']}")
        print(f"    Score    : {r['total_score']}/50  (avg {r['average_score']}/5.0)")
        print(f"    Category : {r['review_category']}")
        print(f"    Strengths: {r['top_strengths']}")
        print(f"    Gaps     : {r['biggest_gaps']}")
        print(f"    Next step: {r['recommended_next_step']}")
    if flagged:
        print("\n-- FLAGGED / DISQUALIFIED --")
        for r in flagged:
            print(f"\n  {r['applicant_name']} — {r['business_name']}")
            print(f"    Reason(s): {r['disqualifier_flags']}")
    print("\n" + "=" * 60)
    print("  WARNING: AI scores are for committee reference only.")
    print("  All selections require human review and final committee approval.")
    print("=" * 60 + "\n")


def main():
    if len(sys.argv) < 2:
        print("Usage: python score.py <input_csv> [output_csv]")
        sys.exit(1)
    input_path  = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "cte_scored_output.csv"
    if not Path(input_path).exists():
        print(f"Error: File not found — {input_path}")
        sys.exit(1)
    results = score_applicants(input_path)
    write_output(results, output_path)
    print_summary(results)
    print(f"Results saved to: {output_path}")


if __name__ == "__main__":
    main()
