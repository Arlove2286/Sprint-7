# FitnessHub: Retention, Revenue and Acquisition Payback

A Power BI review of customer subscription behavior and the relationship between growth and acquisition spending.

## Executive findings

FitnessHub’s main retention challenge appears around **three months after the first subscription payment**. Among cohorts with sufficient follow-up, the retention matrix shows approximately **78% remaining at month index 2 and 50% at index 3**. This roughly 28-percentage-point reduction places the largest early drop between the third and fourth payment months. Engagement efforts should therefore begin before customers reach their fourth renewal period.

The supplied Power BI forecast projects **2,682,598 currency units** in subscription revenue over **February 2026–January 2027**, equivalent to approximately **223,550 per month**. The projected path generally rises, with a small decline in December followed by a January recovery. This is consistent with modest seasonal variation, although a 12-month seasonality setting and just 25 historical months do not establish a strong recurring annual pattern.

Acquisition payback differs across the two annual cohorts. The **2024 cohort crosses its CAC benchmark at month index 7—the eighth payment month**. The **2025 cohort has not recovered its total acquisition cost within the recorded period**. Its shorter observation window limits the conclusion: the data show that payback has not yet been observed, not that recovery is impossible.

Together, these results support a focus on retaining existing subscribers while tracking acquisition efficiency. Rising revenue alone is insufficient evidence of profitable growth, especially because this comparison does not deduct operating or service-delivery costs.

## Report pages and interpretation

### Customer Cohort

Customers are assigned to the month of their first subscription transaction. Each row follows that group across subscription tenure, while the color scale highlights changes in the proportion still making subscription payments.

- **Index 0** represents the initial payment month; index 3 represents the fourth payment month.
- Missing future observations remain blank rather than being counted as zero retention.
- Payment activity serves as a retention proxy. The workbook does not provide explicit cancellation dates or a separate signup-date field.

Consequently, the three-month finding describes the main observed drop-off in payment retention, rather than an exact cancellation date for every customer. FitnessHub should test onboarding improvements, personalized check-ins and renewal reminders during the first three months.

### Revenue Forecast

The monthly chart uses **dim_date[StartOfMonth]** on a **continuous X-axis** and **Subscription Revenue** as the plotted measure. Only subscription transactions contribute to the revenue series.

| Forecast option | Configuration |
|---|---|
| Horizon | 12 months |
| Seasonality | 12 |
| Confidence interval | 95% |
| Ignore last | 0 |

The saved forecast export contains a January 2026 historical anchor. That row is excluded when calculating the following 12-month outlook.

| Forecast month | Expected subscription revenue |
|---|---:|
| February 2026 | 178,248 |
| March 2026 | 186,133 |
| April 2026 | 194,569 |
| May 2026 | 202,828 |
| June 2026 | 215,479 |
| July 2026 | 222,543 |
| August 2026 | 230,046 |
| September 2026 | 238,054 |
| October 2026 | 246,769 |
| November 2026 | 256,385 |
| December 2026 | 252,420 |
| January 2027 | 259,124 |
| **Total** | **2,682,598** |

The monthly uncertainty band expands further into the forecast. Its upper and lower bounds apply to individual months and should not be interpreted as an annual-total confidence interval. Forecast amounts retain the whole-unit precision of the supplied Power BI export. No currency symbol is used because the dataset does not identify a currency.

### CAC vs. LTV

This page compares accumulated subscription revenue for an acquisition cohort against its total customer acquisition cost. Here, LTV is expressed as **aggregate cohort revenue**, making it comparable with aggregate CAC; it is not an estimate of individual customer profit.

| Cohort year | Customer count | Acquisition cost | Observed recovery |
|---|---:|---:|---|
| 2024 | 2,816 | 501,536.80 | Index 7 / eighth payment month |
| 2025 | 6,484 | 1,162,459.11 | Not reached in the available data |

For 2024, cumulative subscription revenue increases from **487,683 at index 6** to **532,921 at index 7**, crossing the **501,536.80** benchmark. The available 2025 series ends at **1,063,636**, below its **1,162,459.11** acquisition cost.

Use the single-select cohort-year filter to compare the groups. The **Total CAC** measure supplies a constant reference line, while cumulative subscription revenue forms the changing curve. CAC is counted once per customer, rather than once per transaction.

Later tenure values have incomplete follow-up, particularly for 2025: only earlier signups have reached those ages. They must not be read as the final lifetime results of the entire cohort. These revenue-based payback calculations also exclude margins and delivery expenses.

## Data structure and calculation approach

The workbook contains `customers` and `transactions`. The existing project documents **9,300 customers**, **64,979 total transactions**, and **51,982 subscription transactions**, covering January 2024 through January 2026.

| Model relationship | Cardinality |
|---|---|
| customers[Customer_ID] → transactions[Customer_ID] | One-to-many |
| dim_date[Date] → transactions[Transaction_Date] | One-to-many |

`Transaction_Date` is treated as a date. The calendar table, `dim_date`, is constructed with `ADDCOLUMNS()` and `CALENDAR()`. Its `StartOfMonth` column supplies the first calendar day of each date’s month. A disconnected tenure table supports the month-index analysis.

Cohort membership is based on the first subscription-payment month. Retention measures continuing payment participation relative to the original cohort; cumulative LTV adds subscription revenue across its members. Non-subscription purchases are excluded from the subscription analysis.

## Repository contents

| Location | Purpose |
|---|---|
| `report.pbix` | Interactive Power BI report |
| `data/Fitness_Subscriptions_Dataset.xlsx` | Original input workbook |
| `screenshots/` | Cohort, forecast, payback and model images |
| `analysis/cohort_retention.csv` | Monthly retention matrix |
| `analysis/cac_ltv.csv` | Acquisition cost and cumulative revenue by tenure |
| `analysis/power_bi_forecast_export.csv` | Supplied visual export, including historical values and bounds |
| `analysis/forecast_12_months.csv` | Future forecast months only |
| `scripts/check_analysis.py` | Independent checks and summary of the CSV exports |

## Opening the report and checking results

Open `report.pbix` in Power BI Desktop and navigate to **Customer Cohort**, **Revenue Forecast**, or **CAC vs. LTV**. The saved data can be viewed without refreshing. To refresh, update the Excel source location to the workbook’s path on your computer.

Run the supplementary checks from the repository folder with Python 3; no additional packages are required:

```bash
python scripts/check_analysis.py
```

The script verifies that the 12 forecast rows match the corresponding visual export, totals the forecast, identifies the first observed CAC crossing for each year, and summarizes the early retention change. It reads the supplied exports without editing them. It does not rebuild the Power BI report or independently fit a forecasting model.

**Screenshot limitation:** `screenshots/data_model.png` is a logical relationship diagram, not an actual Power BI Model view capture. An authentic Model view screenshot is still needed to satisfy that submission requirement. The supplied report and screenshot files have been retained unchanged in this revision.
