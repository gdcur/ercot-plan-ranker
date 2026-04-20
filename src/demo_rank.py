import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
USAGE_CSV = ROOT / "data" / "sample" / "power_usage_15min.csv"
PLANS_CSV = ROOT / "data" / "sample" / "plans.csv"
WEATHER_CSV = ROOT / "data" / "sample" / "weather_daily.csv"
REPORT_OUT = ROOT / "reports" / "demo_ranking.csv"

def read_usage_kwh(path: Path) -> float:
    total = 0.0
    with path.open(newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            total += float(row["usage_kwh"])
    return total

def read_plans(path: Path):
    with path.open(newline="") as f:
        return list(csv.DictReader(f))

def read_weather_cdd(path: Path):
    cdds = []
    with path.open(newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            cdds.append(float(row["cdd_65"]))
    if not cdds:
        raise ValueError("weather file has no rows")
    return cdds

def scenario_factor(cdd_baseline: float, cdd_hot: float) -> float:
    """
    Very simple demo model:
    +3% usage per CDD above baseline (clamped at minimum 1.0).
    """
    factor = 1.0 + 0.03 * (cdd_hot - cdd_baseline)
    return max(1.0, factor)

def main():
    total_kwh = read_usage_kwh(USAGE_CSV)
    plans = read_plans(PLANS_CSV)
    cdds = read_weather_cdd(WEATHER_CSV)

    cdd_baseline = sum(cdds) / len(cdds)
    cdd_hot = max(cdds)
    hot_factor = scenario_factor(cdd_baseline, cdd_hot)

    rows = []
    for p in plans:
        rate = float(p["energy_rate_per_kwh"])
        fixed = float(p["fixed_monthly_charge"])

        kwh_normal = total_kwh
        kwh_hot = total_kwh * hot_factor

        cost_normal = kwh_normal * rate + fixed
        cost_hot = kwh_hot * rate + fixed

        rows.append({
            "plan_id": p["plan_id"],
            "plan_name": p["plan_name"],
            "total_kwh_sample": round(total_kwh, 3),
            "cdd_baseline": round(cdd_baseline, 2),
            "cdd_hot": round(cdd_hot, 2),
            "hot_factor": round(hot_factor, 3),
            "energy_rate_per_kwh": rate,
            "fixed_monthly_charge": fixed,
            "estimated_cost_normal_usd": round(cost_normal, 2),
            "estimated_cost_hot_usd": round(cost_hot, 2),
        })

    # Rank by hot scenario (more conservative than "cheapest in normal")
    rows.sort(key=lambda x: x["estimated_cost_hot_usd"])

    REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
    with REPORT_OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    print(f"Wrote: {REPORT_OUT}")
    print(f"Top plan (ranked by hot scenario): {rows[0]['plan_name']} (${rows[0]['estimated_cost_hot_usd']})")

if __name__ == "__main__":
    main()