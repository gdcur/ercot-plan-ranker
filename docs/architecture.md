# Architecture

This repo shows two views of the same idea:

1) **Current MVP**: what you can run right now
2) **Target state**: where this naturally grows if you keep building

The MVP is deliberately simple so it’s easy to understand. The target state is the “grown-up” version you’d build on a team.

---

## 1) Current MVP (today)

**What it’s for:** take a usage profile, compare plans, and rank by normal vs hot scenario cost.

**Flow**
- Read sample 15-min usage
- Read sample plans
- Compute a simple cost per plan (flat rate + fixed charge)
- Write a ranked CSV report

```mermaid
flowchart LR
  U[data/sample/power_usage_15min.csv] --> P[Python<br/>src/demo_rank.py]
  PL[data/sample/plans.csv] --> P
  P --> R[reports/demo_ranking.csv]
```

**What’s missing (on purpose)**
- tiers, usage credits, minimum usage
- TDU charges, taxes/fees
- time-of-use pricing
- deeper weather normalization (fit usage vs CDD, seasonal effects, station selection)
- regret/robustness metrics

---

## 2) Target state (next evolutions)

**What it’s for:** model plans realistically and compute decision metrics, using a layered lakehouse pattern.

### Components (plain language)
- **Sources:** interval usage, weather, EFL plan documents, reference data
- **Airflow:** runs ingestion, refreshes, and backfills
- **Postgres layers**
  - **Bronze:** raw ingests, append-only + audit columns
  - **Silver:** cleaned and conformed entities (usage, weather, plans)
  - **Gold:** analytics-ready marts (monthly costs, rankings, metrics)
- **dbt:** transformations + tests + docs
- **Spark (optional):** heavy step (example: EFL parsing / pricing normalization)
- **BI tools:** Superset / Grafana / Metabase

### Data flow

```mermaid
flowchart LR
  subgraph S[Sources]
    U[Interval usage]
    W[Weather]
    E[EFL / Plans]
    R[Reference data]
  end

  subgraph O[Orchestration]
    A[Airflow]
  end

  subgraph D[Postgres]
    BR[(Bronze)]
    SI[(Silver)]
    GO[(Gold)]
  end

  T[dbt<br/>transforms + tests]
  SP[Spark optional<br/>EFL parsing / normalization]
  M[Decision metrics<br/>regret, volatility, robustness]
  BI[BI tools<br/>Superset / Grafana / Metabase]

  U --> A
  W --> A
  E --> A
  R --> A

  A --> BR
  BR --> T --> SI
  SI --> SP --> SI
  SI --> T --> GO
  GO --> M --> BI
  GO --> BI
```

---

## 3) Roadmap mapping (MVP → target)

- Pricing realism: tiers, credits, TOU, TDU, fees, taxes
- Scenarios: normal vs hot vs extreme, rolling windows
- Metrics: worst-case regret, average regret, robustness
- Ops: audits, backfills, tests, freshness checks, observability
- Delivery: dashboards and optional API endpoints
