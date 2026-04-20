# Sample data (synthetic)

This folder contains **synthetic sample files** so the repo can stay public and runnable.
They mirror the *shape* of real inputs (usage, plan terms, weather) without exposing any customer or utility data.

## Files

- `power_usage_15min.csv`
  - Synthetic 15-minute interval usage (`usage_kwh`), currently generated for a **1-week** period.
  - Used by the demo to compute `total_kwh_sample`.

- `plans.csv`
  - Sample plan list with the simplified fields used by the MVP:
    - `energy_rate_per_kwh`
    - `fixed_monthly_charge`
  - In the roadmap, this evolves into full EFL parsing (tiers, credits, TDU, fees, etc.).

- `weather_daily.csv`
  - Sample daily weather with `avg_temp_f` and `cdd_65` (Cooling Degree Days, base 65F).
  - Used to build the “normal vs hot” scenario by scaling usage based on higher CDD.

## Notes

- The goal is transparency: the demo is easy to run and easy to extend.
- Data here is synthetic by design; replace it with your own interval usage and real weather sources when validating the approach.