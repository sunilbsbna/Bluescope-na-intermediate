---
name: quality-grading
description: "Grade steel coils using surface defect score, dimensional accuracy percentage, and coating uniformity score. Use for coil quality assessment, Premium/Standard/Economy assignment, grading explanations, validation checks, and repeatable quality review workflows."
argument-hint: "Describe the coil scores or quality inspection data to grade"
user-invocable: true
---

# Quality Grading

Assign a steel coil quality grade from three inspection metrics:

- Surface defect score from 0 to 100, where higher is better
- Dimensional accuracy percentage from 0 to 100, where higher is better
- Coating uniformity score from 0 to 100, where higher is better

This skill is for repeatable coil quality assessment and produces a grade, the decision path, and the validation checks that justify the result.

## When to Use

Use this skill when you need to:

- Grade a steel coil as Premium, Standard, or Economy
- Apply a consistent quality review process to coil inspection data
- Explain why a coil received a given grade
- Validate that inspection inputs are complete and within allowed ranges
- Turn numeric quality measurements into a business-facing quality label

## Required Inputs

Collect these three inputs before grading:

- `surface_defect_score`
- `dimensional_accuracy_percentage`
- `coating_uniformity_score`

Expected ranges:

- `surface_defect_score`: 0 to 100
- `dimensional_accuracy_percentage`: 0 to 100
- `coating_uniformity_score`: 0 to 100

## Validation Rules

Before assigning a grade, validate the input data:

1. Confirm all three scores are present.
2. Confirm each score is numeric.
3. Confirm each score is between 0 and 100 inclusive.
4. Reject the grading request if any score is missing, non-numeric, or outside the valid range.
5. If source measurements are available, ensure the summarized scores came from the latest inspection and use a consistent scoring method.

Do not assign a business grade from partial or invalid data.

## Grading Rules

Apply the grade using the strict threshold rules below.

### Premium

Assign `Premium` when all three scores are greater than or equal to 95.

Rule:

```text
surface_defect_score >= 95
and dimensional_accuracy_percentage >= 95
and coating_uniformity_score >= 95
```

### Standard

Assign `Standard` when all three scores are greater than or equal to 80 and at least one score is below 95.

Rule:

```text
surface_defect_score >= 80 and surface_defect_score < 95
or dimensional_accuracy_percentage >= 80 and dimensional_accuracy_percentage < 95
or coating_uniformity_score >= 80 and coating_uniformity_score < 95
```

Decision guard:

- All three scores must be at least 80
- If all three are at least 95, the grade is Premium instead

### Economy

Assign `Economy` when any one of the three scores is below 80.

Rule:

```text
surface_defect_score < 80
or dimensional_accuracy_percentage < 80
or coating_uniformity_score < 80
```

## Decision Procedure

Follow this workflow every time:

1. Gather the three required scores.
2. Validate that each score is numeric and between 0 and 100.
3. Check for Economy first by testing whether any score is below 80.
4. If not Economy, check for Premium by testing whether all scores are at least 95.
5. If not Premium and all scores are at least 80, assign Standard.
6. Return the final grade with a short explanation that cites the threshold checks.

## Output Format

When using this skill, return:

- Final grade
- The three input scores
- A short explanation of which rule matched
- Any validation issues if grading could not be completed

Suggested response structure:

```text
Grade: Premium
Surface defect score: 97
Dimensional accuracy percentage: 96
Coating uniformity score: 99
Reason: All three scores are at least 95, so the coil qualifies for Premium.
```

## Usage Examples

### Example 1: Premium Coil

Input:

- `surface_defect_score = 98`
- `dimensional_accuracy_percentage = 97`
- `coating_uniformity_score = 96`

Result:

```text
Grade: Premium
Reason: All three scores are greater than or equal to 95.
```

### Example 2: Standard Coil

Input:

- `surface_defect_score = 92`
- `dimensional_accuracy_percentage = 88`
- `coating_uniformity_score = 84`

Result:

```text
Grade: Standard
Reason: All three scores are at least 80, and at least one score is below 95.
```

### Example 3: Economy Coil

Input:

- `surface_defect_score = 93`
- `dimensional_accuracy_percentage = 78`
- `coating_uniformity_score = 90`

Result:

```text
Grade: Economy
Reason: At least one score is below 80.
```

### Example 4: Invalid Input

Input:

- `surface_defect_score = 101`
- `dimensional_accuracy_percentage = 88`
- `coating_uniformity_score = 90`

Result:

```text
Validation error: surface_defect_score must be between 0 and 100.
```

## Example Prompts

- `/quality-grading Grade this coil: surface 97, dimensional 96, coating 95`
- `/quality-grading Determine the quality grade for a coil with surface 82, dimensional 88, coating 91`
- `/quality-grading Validate and grade this inspection: surface 76, dimensional 93, coating 89`
- `/quality-grading Explain why this coil is Economy with scores 79, 92, 90`

## Quality Checks

Before finishing, confirm:

- The skill used all three required metrics
- The inputs were validated before grading
- The grade matched the threshold rules exactly
- The explanation names the threshold that determined the result

## Ambiguities To Confirm Later

If this skill is expanded beyond the current fixed rules, clarify:

- Whether the thresholds should stay global or vary by customer specification
- Whether a future version should accept raw inspection measurements and calculate the three summary scores automatically
- Whether manual override rules should be part of this skill or handled by a separate workflow
