## Approach

My approach to this assignment was to treat the win-rate decline as a decision intelligence problem rather than a pure machine learning task. Instead of focusing on complex predictive modeling, I prioritized interpretability and business usefulness for a CRO audience. I began by framing the core issue as a breakdown in conversion quality despite healthy pipeline volume, and then performed exploratory analysis comparing the two most recent complete quarters to identify where performance shifted. To make the insights more actionable, I designed custom metrics such as Quality-Adjusted Pipeline Inflow (QAPI) to measure pipeline quality beyond raw volume, and a Win Rate Shock Index (WRSI) to detect unusually sharp segment-level declines. I then built a lightweight driver-based decision engine that ranks the key factors impacting win rate across lead sources, regions, and product types, producing outputs that directly map to leadership actions. Finally, I proposed a scalable alerting and insight system design to demonstrate how SkyGeni could productize these diagnostics in a real-world sales intelligence platform.

## How to Run the Project

This project can be executed in two simple ways depending on your preferred workflow:

- **Option 1:** Run interactively in a Jupyter Notebook / Google Colab  
- **Option 2:** Run as a Python script using VS Code or any terminal  

---

### Step 0 — Download or Clone the Repository

First, download the repository ZIP from GitHub **or** clone it:

```bash
git clone <your-repo-url>
cd skygeni-sales-intelligence
```

Make sure the dataset is present in:

```
data/skygeni_sales_data.csv
```

---

## Option 1 — Run in Jupyter Notebook / Google Colab (Recommended for Review)

If you want to explore the analysis step-by-step:

1. Open **Jupyter Notebook** locally or upload the repo to **Google Colab**
2. Open a new notebook (e.g., `notebooks/EDA_Run.ipynb`)
3. Copy the code from:

```
src/part2_eda_insights.py
```
4. Paste it into notebook cells and run sequentially

This will display:

- Win rate summaries  
- Driver tables (Lead Source, Region, Product Type)  
- QAPI + WRSI custom metrics

5. Make sure the dataset file is also in the correct path. In case of google colab you can upload the file in your drive or temporarily upload in the colab from the files menu in the left toolbar (the files will be present only till the runtime is active)  

### Output Location

Charts are automatically saved under:

```
outputs/charts/
   win_rate_trend.png
   win_rate_by_lead_source.png
   win_rate_by_region.png
```

In Google Colab, these generated files can be found in the **Files section on the left toolbar**.

---

## Option 2 — Run as a Python Script (VS Code / Terminal)

For a clean end-to-end execution:

### 1. Install Dependencies

Create an environment (optional) and install required packages:

```bash
pip install pandas numpy matplotlib
```

---

### 2. Run the Insight Engine

Execute the Part 2 CRO diagnostic report:

```bash
python src/part2_eda_insights.py
```

---

### What You Will See

Running the script prints:

- Baseline vs Recent win rate comparison  
- Ranked driver tables for win rate decline  
- Custom pipeline quality metrics (QAPI, WRSI)  
- CRO action checklist  

---

### Output Files Generated

All charts are saved automatically to:

```
outputs/charts/
```

These visualizations support the written submission report.

## Key Decisions

- **Prioritized decision intelligence over complex modeling:**  
  The CRO’s core need was understanding *why* win rate declined, not building a high-accuracy black-box predictor. I therefore focused on interpretable diagnostics rather than advanced ML.

- **Used quarter-over-quarter framing aligned with business workflows:**  
  I compared the two most recent complete quarters (Baseline = 2024Q1, Recent = 2024Q2) since CROs typically evaluate performance in quarterly revenue cycles. Partial-quarter data (2024Q3) was excluded to avoid misleading trends.

- **Designed custom metrics beyond standard win rate reporting:**  
  To make insights more actionable, I introduced:
  - **QAPI (Quality-Adjusted Pipeline Inflow)** to measure pipeline quality, not just volume  
  - **WRSI (Win Rate Shock Index)** to flag unusually sharp segment-level declines

- **Built a lightweight, rule-based driver engine for interpretability:**  
  Instead of training complex models, I implemented a driver attribution system based on win-rate change, business impact contribution, and shock scoring, making outputs directly usable by sales leadership.

- **Focused insights on actionable levers (channel, region, product):**  
  The analysis highlights the specific segments driving decline (e.g., inbound, India region, Core/Pro motions) and translates them into concrete CRO actions.

- **Designed with productization in mind:**  
  The mini system design includes how SkyGeni could operationalize these insights through automated alerts, dashboards, and recurring revenue reviews.

