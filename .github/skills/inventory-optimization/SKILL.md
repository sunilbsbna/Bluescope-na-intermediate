---
name: inventory-optimization
description: Optimize inventory levels and reorder points
---

# Inventory Optimization Skill

Provides recommendations for optimal inventory management.

## Capabilities

- Calculate reorder points
- Suggest optimal stock levels
- Identify slow-moving inventory
- Forecast demand

## Usage

Invoke when:

- Planning inventory levels
- Analyzing stock turnover
- Optimizing warehouse space

## Examples

Calculate reorder point for:

- Product: STL-001
- Lead time: 7 days
- Daily usage: 5 units
- Safety stock: 20 units

## Formula

Reorder Point = (Lead Time × Daily Usage) \* Seasonality Factor + Safety Stock

Determine the Seasonality Factor based on the current month using the seasonality rules defined in `seasonality.md`.
