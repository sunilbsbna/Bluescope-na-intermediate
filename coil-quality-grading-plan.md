# Coil Quality Grading Plan

## Overview

This document defines the proposed coil quality grading feature for the BlueScope steel inventory API. The feature adds coil-specific quality metrics, deterministic grading logic, validation rules, and API support for assigning and retrieving grades.

The grading system uses three business grades:

- Premium
- Standard
- Economy

These align with existing repository conventions:

- Premium = aerospace and automotive applications
- Standard = construction and general manufacturing
- Economy = non-critical applications

The current API already includes a top-level `quality_grade` field on inventory products. The recommended design is to keep that field as the summary outcome while introducing a coil-specific quality assessment payload that drives grade assignment.

## Goals

- Support quality inspection and grading for coil products.
- Keep grade assignment deterministic and auditable.
- Prevent incomplete, contradictory, or invalid inspection data from producing misleading grades.
- Preserve compatibility with the current inventory product model.

## 1. Data Fields To Track

Quality metrics should be stored only for products where `shape == "coil"`.

### 1.1 Inspection Metadata

Add metadata that identifies how and when the inspection occurred:

- `inspection_id`
- `inspected_at`
- `inspector_name`
- `source_system`
- `notes`
- `grading_version`
- `manual_override`
- `override_reason`
- `last_graded_at`

Purpose:

- Support traceability
- Distinguish computed grades from manually overridden grades
- Preserve audit history and rule versioning

### 1.2 Surface Defect Metrics

Track visible and functional surface quality indicators:

- `defect_count`
- `critical_defect_count`
- `scratch_severity`
- `dent_severity`
- `edge_damage_severity`
- `stain_or_contamination_severity`
- `rust_or_corrosion_severity`
- `surface_defect_score`

Recommended conventions:

- Severity values use a bounded scale, such as `0-5`
- Counts are non-negative integers
- `critical_defect_count` captures defects that should block Premium qualification

### 1.3 Dimensional Accuracy Metrics

Track target dimensions, measured values, and tolerance performance:

- `target_width_mm`
- `measured_width_mm`
- `width_deviation_mm`
- `allowed_width_tolerance_mm`
- `target_thickness_mm`
- `measured_thickness_mm`
- `thickness_deviation_mm`
- `allowed_thickness_tolerance_mm`
- `target_length_mm`
- `measured_length_mm`
- `length_deviation_mm`
- `allowed_length_tolerance_mm`
- `camber_mm`
- `allowed_camber_mm`
- `flatness_mm`
- `allowed_flatness_mm`
- `dimensional_score`

Purpose:

- Measure conformance to customer or product specification
- Support tight-vs-standard tolerance bands for different grades
- Make grading explainable using objective dimensional checks

### 1.4 Coating Uniformity Metrics

Track coating quality for coated coils:

- `coating_required`
- `target_coating_gsm`
- `average_coating_gsm`
- `min_coating_gsm`
- `max_coating_gsm`
- `coating_variation_percent`
- `bare_spot_count`
- `adhesion_issue_count`
- `coating_score`

Purpose:

- Evaluate whether coating meets target mass and consistency requirements
- Capture defects that affect corrosion protection or customer suitability
- Allow Premium grading to require tighter coating uniformity than Standard

### 1.5 Derived Grading Outputs

Store calculated outputs and reasons, not just the final label:

- `overall_quality_score`
- `quality_grade`
- `grading_reasons`
- `failed_rules`
- `computed_quality_grade`
- `override_quality_grade`

Purpose:

- Make decisions auditable
- Support debugging and rule refinement
- Preserve both computed and overridden outcomes

## 2. Business Logic For Grade Assignment

The grading engine should be rule-based and deterministic. Clients should not directly assign a final grade except through an explicit manual override workflow.

### 2.1 Core Principles

- Grade assignment must be reproducible from the same inspection inputs.
- The server computes the grade.
- Thresholds and scoring rules should live in one grading service or configuration object.
- Any update to quality metrics should trigger regrading.
- The API should return both the assigned grade and the reason codes.

### 2.2 Category Weights

Recommended overall weighting:

- Surface defects: 40%
- Dimensional accuracy: 35%
- Coating uniformity: 25%

These weights reflect the operational importance of visible and functional defects, dimensional conformance, and coating consistency.

### 2.3 Premium Grade Rules

Premium should represent the highest-quality coils suitable for aerospace and automotive use.

Suggested requirements:

- No critical surface defects
- Very low minor defect severity
- All measured dimensions within tight tolerance bands
- Minimal camber and flatness deviation
- Coating variation tightly controlled
- No bare spots
- No adhesion failures
- Overall score in the top scoring band

Premium should fail immediately if any hard-stop condition is present, such as a critical defect or a major tolerance breach.

### 2.4 Standard Grade Rules

Standard should represent acceptable commercial quality for construction and general manufacturing.

Suggested requirements:

- No disqualifying critical defects
- Minor cosmetic defects allowed within defined limits
- Dimensions within normal production tolerances
- Moderate coating variation allowed when still fit for intended use
- Overall score in the mid scoring band

Standard should allow acceptable process variation without collapsing into Economy.

### 2.5 Economy Grade Rules

Economy should represent usable but lower-quality product for non-critical applications.

Suggested requirements:

- Quality issues exceed Standard thresholds but the coil remains saleable and safe
- Cosmetic or dimensional issues are above preferred levels but still within minimum usability limits
- Coating or surface issues are acceptable only for non-critical use cases

Important rule:

- Do not use Economy as a fallback for missing or invalid data.

If required inspection inputs are missing, the system should reject the request or return an explicit ungradable state rather than assigning Economy.

### 2.6 Manual Override Rules

Manual override is allowed only under explicit control.

Requirements:

- Persist both computed and overridden grades
- Require `override_reason`
- Capture who performed the override and when
- Keep rule-generated reason codes even if an override is applied

## 3. Validation Rules For Data Quality

Validation should occur at three levels:

- Payload structure
- Business plausibility
- Grading integrity

### 3.1 Core Product Validation

- `shape` must be one of the existing allowed values
- Coil quality metrics are only valid when `shape == "coil"`
- `product_code` remains required and should be unique
- `length_mm`, `thickness_mm`, and optional `width_mm` must be positive
- `quantity` and `min_stock_level` must be non-negative integers
- `quality_grade` must be restricted to `Premium`, `Standard`, or `Economy`
- Reject coil quality payloads for non-coil products with `422`

### 3.2 Inspection Metadata Validation

- Require `inspected_at`
- Require either `inspector_name` or `source_system`
- Require `grading_version`
- Constrain free-text fields such as `notes` and `override_reason` with maximum lengths

### 3.3 Surface Defect Validation

- `defect_count >= critical_defect_count`
- All count fields must be integers `>= 0`
- All severity fields must stay within the defined range, for example `0-5`
- Reject unknown defect categories if defect type enums are introduced

### 3.4 Dimensional Validation

- `target_*` and `measured_*` values must be positive when provided
- Tolerances must be positive
- `camber_mm` and `flatness_mm` must be non-negative
- Derived deviations should either be computed server-side or validated against target/measured values
- Reject physically implausible values such as zero measured thickness

### 3.5 Coating Validation

- Use `coating_required` to control conditional field requirements
- If `coating_required == true`, require coating measurement fields
- If `coating_required == false`, coating-specific numeric fields should be absent or null
- `min_coating_gsm <= average_coating_gsm <= max_coating_gsm`
- `target_coating_gsm` must be positive
- `coating_variation_percent >= 0`
- `bare_spot_count >= 0`
- `adhesion_issue_count >= 0`

### 3.6 Cross-Field Consistency Rules

- Do not accept partially populated grading sections
- If one grading section is supplied, all required fields for that section must be present
- If `manual_override == true`, require a valid override grade and non-empty `override_reason`
- If `manual_override == false`, override fields should be null or omitted
- `last_graded_at` must not be earlier than `inspected_at`
- Recompute the grade whenever inspection data changes

### 3.7 Grade Integrity Rules

- Clients should not directly submit a final `quality_grade` without the supporting metrics, except through a documented override workflow
- The server computes the grade
- Persist `computed_quality_grade` separately from `override_quality_grade`
- Return explicit reason codes such as `critical_surface_defect`, `width_out_of_tolerance`, or `coating_variation_high`
- If required inputs are missing, return `422` or an explicit ungradable result

## 4. API And Model Changes

The existing API surface is centered on the inventory router and the `SteelProduct` model. The grading design should extend that structure instead of introducing a disconnected subsystem.

### 4.1 Model Changes

Keep the existing top-level product field:

- `SteelProduct.quality_grade`

Add an optional nested coil quality structure:

- `coil_quality`

Recommended new models:

- `CoilSurfaceMetrics`
- `CoilDimensionalMetrics`
- `CoilCoatingMetrics`
- `CoilQualityMetrics`
- `CoilQualityAssessmentRequest`
- `CoilQualityAssessmentResponse`

Design intent:

- `SteelProduct` stores the summary quality result
- `coil_quality` stores the supporting inspection metrics and grading outputs

### 4.2 Endpoint Changes

Recommended endpoints:

- `POST /inventory/{product_id}/grading`
- `GET /inventory/{product_id}/grading`
- `PATCH /inventory/{product_id}/grading`

Endpoint purposes:

- `POST` computes and persists a new grading assessment for an existing coil
- `GET` returns the latest grading inputs, scores, grade, and reasons
- `PATCH` updates assessment inputs and triggers recalculation

Optional filtering enhancement:

- `GET /inventory/?quality_grade=Premium&shape=coil`

This allows downstream users to filter premium-quality coils directly from inventory queries.

### 4.3 Persistence Changes

The in-memory database should be updated to:

- Store nested `coil_quality` data
- Update `last_updated` when grading data changes
- Preserve computed and overridden grade outputs

### 4.4 Response Requirements

Responses should include:

- Final quality grade
- Computed quality grade
- Override quality grade if present
- Overall score
- Category scores
- Reason codes
- Failed rule identifiers
- Inspection metadata

This is necessary for auditability and downstream operational decisions.

## 5. Testing Requirements

Add focused tests that validate both rule behavior and data quality boundaries.

### 5.1 Validation Tests

- Reject coil quality payloads for non-coil products
- Reject missing required coating fields when coating is required
- Reject invalid severity ranges
- Reject invalid score ranges
- Reject inconsistent coating statistics such as average outside min/max
- Reject override requests without a reason
- Reject incomplete inspection sections

### 5.2 Grading Logic Tests

- Premium boundary case passes
- Premium disqualified by critical defect
- Standard boundary case passes
- Economy assigned for usable but lower-quality coil
- Missing required grading data does not silently assign Economy
- Manual override preserves both computed and overridden grades

### 5.3 Endpoint Tests

- Create or update grading for an existing coil
- Reject grading requests for non-coil products
- Return `404` for missing product IDs
- Return persisted grading data via `GET /inventory/{product_id}/grading`
- Regrade when grading inputs change

## 6. Recommended Implementation Order

1. Add the new Pydantic models and validation rules.
2. Implement a dedicated grading utility or service that computes category scores, overall score, reason codes, and final grade.
3. Extend the database layer to store nested coil quality data and update timestamps correctly.
4. Add grading endpoints to the inventory router.
5. Add boundary-focused automated tests for validation and grade assignment.
6. Refine threshold values after test coverage is in place.

## 7. Summary Of Requirements

To implement coil quality grading correctly, the system needs:

- Coil-specific inspection data fields
- Deterministic grade assignment rules
- Strong validation for structural and business correctness
- API endpoints for grading create, read, and update flows
- Storage of both summary grade and detailed inspection data
- Audit-friendly responses with reasons and failed rules
- Tests covering both validation and grade boundaries

This design keeps compatibility with the existing inventory model while making coil quality decisions explainable, consistent, and production-ready.
