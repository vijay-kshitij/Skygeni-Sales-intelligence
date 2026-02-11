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
4. Make sure the dataset file is also in teh correct path. In case of google colab you can upload the file in your drive or temporarily upload in the colab from the files menu in the left toolbar (the files will be present only till the runtime is active)
5. Paste it into notebook cells and run sequentially

This will display:

- Win rate summaries  
- Driver tables (Lead Source, Region, Product Type)  
- QAPI + WRSI custom metrics  

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

---

✅ Both workflows reproduce the full Part 2 analysis used in the final submission.
