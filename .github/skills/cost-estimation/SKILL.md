---
name: cost-estimation
description: "Calculate steel product costs, shipping expenses, and project estimates. Use for: pricing quotes, material cost analysis, shipping calculations, budget forecasting, total project cost estimation, cost comparisons across steel grades and shapes."
argument-hint: "Describe what to estimate: material costs, shipping, or full project estimate with quantities and specifications"
user-invocable: true
---

# Cost Estimation for Steel Products

Comprehensive cost estimation for steel inventory projects including material costs, shipping expenses, and total project budgets.

## When to Use

Use this skill when you need to:

- Calculate material costs for steel products (sheets, plates, coils, bars, tubes)
- Estimate shipping and transportation costs
- Generate project cost estimates with multiple line items
- Compare pricing across different steel grades or suppliers
- Forecast budgets for steel procurement
- Analyze cost per weight ($/kg) or cost per area ($/m²)
- Calculate total landed costs including materials and logistics

## Core Formulas

### Material Cost Calculation

**Basic Material Cost:**

```
Material Cost = Weight (kg) × Price per kg ($/kg)
```

**Alternative by Area (for sheets/plates/coils):**

```
Material Cost = Area (m²) × Price per m² ($/m²)
```

**Weight Calculation (from dimensions):**

- **Sheet/Plate/Coil:** `Weight = Length × Width × Thickness × Density`
- **Bar (circular):** `Weight = π × (Diameter/2)² × Length × Density`
- **Tube (hollow):** `Weight = π × [(Outer_Diameter/2)² - (Inner_Diameter/2)²] × Length × Density`

Where:

- Dimensions in millimeters (mm)
- Steel density ≈ 7.85e-6 kg/mm³ (7850 kg/m³)

### Shipping Cost Calculation

**Distance-Based Shipping:**

```
Shipping Cost = Base Rate + (Distance × Rate per km) + (Weight × Rate per kg)
```

**Flat Rate Shipping:**

```
Shipping Cost = Base Rate × Number of Units
```

**Tiered Shipping (by weight brackets):**

```
if Weight ≤ 500 kg: Shipping Cost = Tier_1_Rate
elif Weight ≤ 2000 kg: Shipping Cost = Tier_2_Rate
else: Shipping Cost = Tier_3_Rate
```

### Total Project Cost

```
Total Cost = Σ(Material Costs) + Σ(Shipping Costs) + Markup/Overhead
```

**With Markup:**

```
Final Price = Total Cost × (1 + Markup Percentage)
```

## Pricing Scenarios

### Scenario 1: Per-Kilogram Pricing

Most common for steel products. Calculate weight first, then apply unit price.

**Example:**

- Product: A36 Steel Plate
- Dimensions: 3000mm × 1500mm × 10mm
- Weight: 3000 × 1500 × 10 × 7.85e-6 = 353.25 kg
- Price: $2.50/kg
- Material Cost: 353.25 × $2.50 = **$883.13**

### Scenario 2: Per-Square-Meter Pricing

Common for sheet and coil products sold by area.

**Example:**

- Product: 304 Stainless Steel Sheet
- Dimensions: 2500mm × 1200mm (3.0 m²)
- Price: $45/m²
- Material Cost: 3.0 × $45 = **$135.00**

### Scenario 3: Volume Discounts

Tiered pricing based on order quantity.

**Example:**

- Base price: $3.00/kg
- 500-1000 kg: 5% discount → $2.85/kg
- 1000-5000 kg: 10% discount → $2.70/kg
- 5000+ kg: 15% discount → $2.55/kg

### Scenario 4: Grade-Based Pricing

Different steel grades have different base prices.

**Common Price Multipliers (relative to A36):**

- A36 (Carbon Steel): 1.0× (base)
- 304 (Stainless): 3.5× - 4.0×
- 316 (Stainless): 4.5× - 5.0×
- 4140 (Alloy): 2.0× - 2.5×

### Scenario 5: Distance-Based Shipping

Calculate shipping based on distance and weight.

**Example:**

- Base rate: $50
- Distance: 350 km @ $0.15/km
- Weight: 750 kg @ $0.08/kg
- Shipping Cost: $50 + (350 × $0.15) + (750 × $0.08) = $50 + $52.50 + $60 = **$162.50**

## Step-by-Step Estimation Process

### 1. Gather Product Specifications

Collect the following information:

- **Shape:** sheet, plate, coil, bar, or tube
- **Dimensions:** length, width (if applicable), thickness
- **Steel Grade:** A36, 304, 316, 4140, etc.
- **Quantity:** number of units or total tonnage
- **Delivery Location:** for shipping calculations

### 2. Calculate Material Weight

Use the weight calculation formulas based on shape:

```python
# Example for plate
length_mm = 3000
width_mm = 1500
thickness_mm = 10
density = 7.85e-6  # kg/mm³

weight_kg = length_mm * width_mm * thickness_mm * density
```

For multiple items, sum the total weight.

### 3. Apply Pricing Model

Determine which pricing model applies:

- Per-kilogram pricing
- Per-square-meter pricing
- Volume discount tiers
- Grade-based pricing adjustments

Calculate material cost accordingly.

### 4. Calculate Shipping Costs

Determine shipping method and calculate:

- Distance-based shipping
- Flat rate shipping
- Tiered weight-based shipping
- Expedited vs. standard shipping

### 5. Add Overhead and Markup

Apply any additional costs:

- Handling fees
- Taxes
- Insurance
- Markup percentage (typically 10-30%)

### 6. Generate Total Estimate

Sum all components:

```
Total Estimate = Material Cost + Shipping Cost + Overhead + Markup
```

## Usage Examples

### Example 1: Simple Material Cost

**Request:** "Estimate the cost for a 4000mm × 2000mm × 12mm A36 steel plate at $2.80/kg"

**Calculation:**

1. Weight = 4000 × 2000 × 12 × 7.85e-6 = 753.60 kg
2. Material Cost = 753.60 × $2.80 = $2,110.08

**Result:** $2,110.08

### Example 2: Material + Shipping

**Request:** "Quote for 5 sheets of 304 stainless steel (2500mm × 1200mm × 3mm) at $50/m², shipping to a location 280km away"

**Calculation:**

1. Area per sheet = 2.5m × 1.2m = 3.0 m²
2. Total area = 3.0 × 5 = 15 m²
3. Material Cost = 15 × $50 = $750.00
4. Weight per sheet = 2500 × 1200 × 3 × 7.85e-6 = 70.65 kg
5. Total weight = 70.65 × 5 = 353.25 kg
6. Shipping = $50 base + (280 × $0.15/km) + (353.25 × $0.08/kg)
   = $50 + $42 + $28.26 = $120.26
7. Total Cost = $750.00 + $120.26 = $870.26

**Result:** $870.26

### Example 3: Multi-Product Project Estimate

**Request:** "Estimate total project cost for the following:

- 10× A36 plates (3000×1500×10mm) @ $2.50/kg
- 5× 304 bars (6000mm length, 50mm diameter) @ $8.50/kg
- Shipping: $200 flat rate
- Apply 20% markup"

**Calculation:**

**Plates:**

1. Weight per plate = 3000 × 1500 × 10 × 7.85e-6 = 353.25 kg
2. Total plate weight = 353.25 × 10 = 3,532.5 kg
3. Plate cost = 3,532.5 × $2.50 = $8,831.25

**Bars:**

1. Weight per bar = π × (25)² × 6000 × 7.85e-6 = 92.36 kg
2. Total bar weight = 92.36 × 5 = 461.8 kg
3. Bar cost = 461.8 × $8.50 = $3,925.30

**Total:**

1. Material subtotal = $8,831.25 + $3,925.30 = $12,756.55
2. Shipping = $200.00
3. Subtotal before markup = $12,756.55 + $200.00 = $12,956.55
4. Markup (20%) = $12,956.55 × 0.20 = $2,591.31
5. **Final Total = $15,547.86**

**Breakdown:**

- Materials: $12,756.55
- Shipping: $200.00
- Markup (20%): $2,591.31
- **Grand Total: $15,547.86**

### Example 4: Cost Comparison Across Grades

**Request:** "Compare the cost of a 2000mm × 1000mm × 5mm sheet in different grades"

**Calculation:**

1. Weight = 2000 × 1000 × 5 × 7.85e-6 = 78.5 kg
2. A36 @ $2.50/kg = 78.5 × $2.50 = $196.25
3. 304 @ $9.00/kg = 78.5 × $9.00 = $706.50
4. 316 @ $11.50/kg = 78.5 × $11.50 = $902.75
5. 4140 @ $5.50/kg = 78.5 × $5.50 = $431.75

**Result:**
| Grade | Price/kg | Total Cost |
|-------|----------|------------|
| A36 | $2.50 | $196.25 |
| 304 | $9.00 | $706.50 |
| 316 | $11.50 | $902.75 |
| 4140 | $5.50 | $431.75 |

### Example 5: Volume Discount Scenario

**Request:** "Calculate cost for 2500 kg of A36 steel with volume discounts: 0-500kg: $3.00/kg, 501-1000kg: $2.85/kg, 1001-5000kg: $2.70/kg"

**Calculation:**

1. Quantity: 2500 kg falls in 1001-5000kg tier
2. Applicable price: $2.70/kg
3. Total cost = 2500 × $2.70 = **$6,750.00**
4. Savings vs base price = 2500 × ($3.00 - $2.70) = **$750.00 saved**

**Result:** $6,750.00 (saved $750.00 with volume discount)

## Integration with Steel Inventory API

This skill can work with the existing steel inventory system by:

1. **Retrieving product data** from the inventory database
2. **Calculating weights** using the `steel_utils.py` module
3. **Applying current pricing** from the database
4. **Generating quotes** with real inventory data

**Example API Integration:**

```python
# Use existing weight calculation
from app.utils.steel_utils import calculate_weight_kg

weight = calculate_weight_kg(
    length_mm=3000,
    width_mm=1500,
    thickness_mm=10,
    shape="plate"
)

# Apply pricing
price_per_kg = 2.50
material_cost = weight * price_per_kg
```

## Best Practices

1. **Always round currency** to 2 decimal places
2. **Show unit prices** alongside totals for transparency
3. **Include weight calculations** in the breakdown
4. **Account for waste/scrap** (typically 5-10% extra material)
5. **Document assumptions** (shipping method, lead times, pricing date)
6. **Include disclaimers** for quotes (validity period, price fluctuations)
7. **Provide itemized breakdowns** for complex projects
8. **Consider currency exchange** for international orders

## Common Pricing Variables

**Material Pricing Factors:**

- Base metal commodity prices (fluctuate daily)
- Steel grade/alloy composition
- Product form (sheet vs coil vs bar)
- Thickness (thick plate often costs more per kg)
- Width (non-standard widths may have premiums)
- Finish (mill finish vs polished)
- Quantity (volume discounts)
- Market conditions and availability

**Shipping Cost Factors:**

- Distance from mill/warehouse
- Weight and dimensions
- Delivery urgency (standard vs expedited)
- Special handling requirements
- Fuel surcharges
- Regional factors

## Output Format

Always present estimates in a clear, structured format:

```
COST ESTIMATE

Product Details:
- Type: [product type]
- Dimensions: [length × width × thickness]
- Grade: [steel grade]
- Quantity: [number of units]

Calculations:
- Weight per unit: [X] kg
- Total weight: [Y] kg
- Material cost: $[A] ([price]/kg)
- Shipping cost: $[B]
- Subtotal: $[A + B]
- Markup ([Z]%): $[C]

TOTAL: $[FINAL AMOUNT]

Valid until: [date]
Assumptions: [list key assumptions]
```

## Quick Reference

**Common Steel Densities:**

- Carbon Steel (A36): 7.85 g/cm³ = 7.85e-6 kg/mm³
- Stainless Steel (304/316): 8.00 g/cm³ = 8.00e-6 kg/mm³
- Aluminum: 2.70 g/cm³ = 2.70e-6 kg/mm³

**Typical Markup Ranges:**

- Industrial/Wholesale: 10-15%
- Retail/Small orders: 20-30%
- Specialty/Custom: 30-50%

**Standard Shipping Lead Times:**

- Local (< 100 km): 1-2 days
- Regional (100-500 km): 2-5 days
- National (500+ km): 5-10 days
