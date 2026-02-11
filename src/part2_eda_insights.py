import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from math import sqrt


# ============================================================
# CONFIG (Baseline vs Recent Quarter)
# ============================================================
BASELINE_Q = "2024Q1"
RECENT_Q   = "2024Q2"


# ============================================================
# Load + Prepare Data
# ============================================================
def load_deals(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)

    df["created_date"] = pd.to_datetime(df["created_date"])
    df["closed_date"] = pd.to_datetime(df["closed_date"])

    df["outcome"] = df["outcome"].str.strip().str.title()
    df["is_won"] = (df["outcome"] == "Won").astype(int)

    df["created_q"] = df["created_date"].dt.to_period("Q").astype(str)
    df["closed_q"] = df["closed_date"].dt.to_period("Q").astype(str)

    return df


# ============================================================
# Custom Metric 1: QAPI (skip first quarter)
# ============================================================
def quality_adjusted_pipeline_inflow(df: pd.DataFrame) -> pd.DataFrame:
    segment_cols = ["lead_source", "product_type", "region"]
    quarters = sorted(df["created_q"].unique())

    rows = []

    # Skip first quarter (no historical baseline exists)
    for q in quarters[1:]:
        prior_q = str(pd.Period(q, freq="Q") - 1)

        baseline = df[df["closed_q"] == prior_q]
        if len(baseline) == 0:
            baseline = df[df["closed_q"] < q]

        overall_wr = baseline["is_won"].mean()

        seg_wr = baseline.groupby(segment_cols)["is_won"].mean().reset_index()
        seg_wr.columns = segment_cols + ["segment_win_rate"]

        created = df[df["created_q"] == q].merge(seg_wr, on=segment_cols, how="left")
        created["segment_win_rate"] = created["segment_win_rate"].fillna(overall_wr)

        created["expected_acv"] = created["deal_amount"] * created["segment_win_rate"]

        rows.append({
            "Created Quarter": q,
            "Deals Created": len(created),
            "Pipeline ACV ($M)": created["deal_amount"].sum() / 1e6,
            "QAPI Expected Revenue ($M)": created["expected_acv"].sum() / 1e6
        })

    return pd.DataFrame(rows)


# ============================================================
# Custom Metric 2: WRSI Shock Index
# ============================================================
def win_rate_shock_index(p1, n1, p2, n2):
    pooled = (p1 * n1 + p2 * n2) / (n1 + n2)
    se = sqrt(pooled * (1 - pooled) * (1/n1 + 1/n2))
    return 0 if se == 0 else (p2 - p1) / se


# ============================================================
# Driver Table Generator
# ============================================================
def driver_table(df: pd.DataFrame, column: str):

    base = df[df["closed_q"] == BASELINE_Q]
    recent = df[df["closed_q"] == RECENT_Q]

    g1 = base.groupby(column)["is_won"].agg(["mean", "count"])
    g2 = recent.groupby(column)["is_won"].agg(["mean", "count"])

    table = g1.join(g2, lsuffix="_base", rsuffix="_recent").fillna(0)

    table = table.rename(columns={
        "mean_base": "Baseline Win Rate",
        "count_base": "Baseline Deals",
        "mean_recent": "Recent Win Rate",
        "count_recent": "Recent Deals"
    })

    table["Win Rate Change (pts)"] = (
        table["Recent Win Rate"] - table["Baseline Win Rate"]
    ) * 100

    table["Impact on Overall (pts)"] = (
        table["Baseline Deals"] / table["Baseline Deals"].sum()
    ) * table["Win Rate Change (pts)"]

    table["WRSI Shock Score"] = table.apply(
        lambda r: win_rate_shock_index(
            r["Baseline Win Rate"], r["Baseline Deals"],
            r["Recent Win Rate"], r["Recent Deals"]
        ) if r["Baseline Deals"] > 0 and r["Recent Deals"] > 0 else 0,
        axis=1
    )

    return table.sort_values("Impact on Overall (pts)")


# ============================================================
# Chart Functions
# ============================================================
def plot_win_rate_trend(df):
    trend = df.groupby("closed_q")["is_won"].mean().reset_index()

    # ✅ Remove incomplete quarter (2024Q3)
    trend = trend[trend["closed_q"] <= RECENT_Q]

    plt.figure()
    plt.plot(trend["closed_q"], trend["is_won"] * 100, marker="o")
    plt.xticks(rotation=45)
    plt.ylabel("Win Rate (%)")
    plt.title("Win Rate Trend Over Time")

    os.makedirs("outputs/charts", exist_ok=True)
    plt.savefig("outputs/charts/win_rate_trend.png", dpi=200)
    plt.close()



def plot_segment_comparison(df, column, filename):
    table = driver_table(df, column)

    labels = table.index
    baseline = table["Baseline Win Rate"] * 100
    recent = table["Recent Win Rate"] * 100

    x = np.arange(len(labels))
    width = 0.35

    plt.figure()
    plt.bar(x - width/2, baseline, width, label=BASELINE_Q)
    plt.bar(x + width/2, recent, width, label=RECENT_Q)

    plt.xticks(x, labels)
    plt.ylabel("Win Rate (%)")
    plt.title(f"Win Rate by {column}: Baseline vs Recent")
    plt.legend()

    os.makedirs("outputs/charts", exist_ok=True)
    plt.savefig(f"outputs/charts/{filename}", dpi=200)
    plt.close()


# ============================================================
# CRO-Friendly Report Runner
# ============================================================
def run_report(df):

    print("\n" + "="*75)
    print(" SKYGENI PIPELINE HEALTH REPORT — WIN RATE DIAGNOSIS ")
    print("="*75)
    print(f"Baseline Quarter: {BASELINE_Q}")
    print(f"Recent Quarter:   {RECENT_Q}")

    overall_base = df[df["closed_q"] == BASELINE_Q]["is_won"].mean()
    overall_recent = df[df["closed_q"] == RECENT_Q]["is_won"].mean()

    print("\nOverall Win Rate Change:")
    print(f"{BASELINE_Q}: {overall_base*100:.1f}%")
    print(f"{RECENT_Q}:   {overall_recent*100:.1f}%")
    print(f"Delta: {(overall_recent-overall_base)*100:.2f} pts")

    # Lead Source Drivers
    print("\n" + "-"*75)
    print("INSIGHT DRIVERS — LEAD SOURCE")
    print("-"*75)

    lead_table = driver_table(df, "lead_source")
    print(lead_table.round(2))

    # Region Drivers
    print("\n" + "-"*75)
    print("INSIGHT DRIVERS — REGION")
    print("-"*75)

    region_table = driver_table(df, "region")
    print(region_table.round(2))

    # Product Drivers
    print("\n" + "-"*75)
    print("INSIGHT DRIVERS — PRODUCT TYPE")
    print("-"*75)

    product_table = driver_table(df, "product_type")
    print(product_table.round(2))

    # QAPI
    print("\n" + "-"*75)
    print("PIPELINE QUALITY — QAPI METRIC")
    print("-"*75)

    qapi = quality_adjusted_pipeline_inflow(df)
    print(qapi.round(2))

    print("\nCharts saved to: outputs/charts/")
    print(" - win_rate_trend.png")
    print(" - win_rate_by_lead_source.png")
    print(" - win_rate_by_region.png")

    print("\n" + "="*75)
    print(" CRO ACTION CHECKLIST ")
    print("="*75)
    print("1. Fix inbound lead quality decline")
    print("2. Investigate region-level drops (India focus)")
    print("3. Reassess Core/Pro positioning and objections")
    print("4. Scale referral motion (strongest performer)")
    print("="*75)


# ============================================================
# Main
# ============================================================
if __name__ == "__main__":

    file_path = 'data/skygeni_sales_data.csv'
    df = load_deals(file_path)

    # Generate charts
    plot_win_rate_trend(df)
    plot_segment_comparison(df, "lead_source", "win_rate_by_lead_source.png")
    plot_segment_comparison(df, "region", "win_rate_by_region.png")

    # Run CRO report
    run_report(df)
