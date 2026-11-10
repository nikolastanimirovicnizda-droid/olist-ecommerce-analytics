[README.md](https://github.com/user-attachments/files/34655140/README.md)
# Olist E-Commerce Analytics & Business Performance Report

End-to-end data analytics project on the Brazilian Olist E-Commerce dataset (~100k orders, 2016–2018).
The pipeline covers Python data cleaning, a PostgreSQL star schema, analytical SQL (RFM segmentation, revenue trends, category ranking) and a 4-page interactive Power BI dashboard.

**Tools:** Python (pandas, SQLAlchemy) · PostgreSQL · SQL · Power BI (DAX)

**Dataset:** [Brazilian E-Commerce Public Dataset by Olist (Kaggle)](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

---

## Dashboard Preview

### Executive Overview
![Executive Overview](page1_executive_overview.png)

### Sales Performance
![Sales Performance](page2_sales_performance.png)

### Customer Analysis
![Customer Analysis](page3_customer_analysis.png)

### Operations & Logistics
![Operations](page4_operations.png)

---

## Executive Summary

### 1. Problem Statement

Olist connects small independent merchants across Brazil with large online marketplaces. Rapid growth created several challenges for leadership:

- **Revenue visibility:** difficulty separating seasonal spikes from steady long-term growth.
- **Logistics costs:** high freight rates and longer delivery windows in non-metropolitan regions hurting conversion.
- **Category performance:** limited insight into which product lines drive revenue versus those that only create operational volume.

### 2. Data & Architecture

The raw data consists of 9 CSV files (orders, items, payments, reviews, customers, sellers, products, geolocation, category translations). After cleaning, it is loaded into PostgreSQL staging tables (`stg_*`) and modeled into a star schema:

- **Fact table `fact_orders`** (grain: one row per order item): price, freight, order status and timestamps, plus order-level review score and payment info.
- **Dimensions:**
  - `dim_date`: year, quarter, month, day, weekday, weekend flag
  - `dim_customer`: unique customer ID, city, state, ZIP prefix
  - `dim_product`: English category names and product attributes
  - `dim_geography`: ZIP prefix with average latitude/longitude

> **Modeling note:** `review_score` and `payment_value` are order-level values repeated on every item row of the same order. Do not `SUM` them in DAX (that would double-count multi-item orders); use averages or distinct order-level logic.

### 3. Methodology

1. **Data cleaning (Python):** parsed timestamps, handled missing values, standardized text fields, removed duplicates.
2. **Data loading:** loaded cleaned CSVs into PostgreSQL staging tables.
3. **Modeling (SQL):** built dimensions and the fact table; mapped Portuguese category names to English.
4. **Analysis (SQL):** quarterly/monthly revenue, category ranking, RFM segmentation.
5. **Dashboard (Power BI):** 4 pages with DAX measures and 1-to-many, single-direction relationships between dimensions and the fact table.

### 4. Key Findings

- **Regional concentration:** São Paulo (SP) is the main hub, generating over 40% of order volume and net revenue.
- **Product performance:** Health & Beauty and Bed Bath Table lead order volume, while technical categories such as Computers & Accessories have the highest Average Order Value.
- **Freight impact:** shipping makes up a disproportionately high share of the purchase price in the North and Northeast, dampening sales outside the Southeast.

### 5. Strategic Recommendations

1. **Decentralized logistics:** open regional fulfillment hubs outside São Paulo to cut freight cost and delivery time.
2. **Product bundling:** multi-item bundles for low-priced categories to raise basket size and offset shipping.
3. **Targeted expansion:** focus acquisition on secondary markets such as Rio de Janeiro and Belo Horizonte.

### 6. Limitations

- **Historical scope:** static data ending in 2018, no real-time integration.
- **No cost data:** no seller margins or customer acquisition cost, so profitability cannot be evaluated.
- **Anonymized customers:** no demographic profiling (age, income).
- **Order statuses:** the fact table includes all order statuses (including canceled), so revenue figures reflect orders placed, not only delivered.

---

## KPI Metrics Dictionary

| Metric | DAX | Description | Business Purpose |
|---|---|---|---|
| Total Revenue | `SUM(fact_orders[price])` | Sum of item prices, excluding freight | Tracks gross sales volume |
| Total Orders | `DISTINCTCOUNT(fact_orders[order_id])` | Unique orders | Measures demand and throughput |
| Average Order Value | `DIVIDE([Total Revenue], [Total Orders], 0)` | Revenue per order | Evaluates average customer spend |
| Total Customers | `DISTINCTCOUNT(dim_customer[customer_unique_id])` | Unique buyers | Customer reach without duplicates |
| Total Freight | `SUM(fact_orders[freight_value])` | Sum of shipping charges | Tracks shipping cost by region |

---

## Repository Structure

```
.
├── scripts/                       # Python: data cleaning and loading into PostgreSQL
├── sql/
│   ├── create_analytical_model.sql   # star schema (dimensions + fact table)
│   ├── 01_sales_over_time.sql        # quarterly/monthly revenue
│   ├── 02_product_analysis.sql       # category performance
│   └── 03_customer_analytics.sql     # RFM segmentation
├── olist_analytics_dashboard.pbix # Power BI report
├── page1_executive_overview.png   # dashboard screenshots
├── page2_sales_performance.png
├── page3_customer_analysis.png
├── page4_operations.png
└── README.md
```

> The `data/` folder (raw and processed CSVs) is not included in the repository. Download the dataset from Kaggle (link above).

---

## How to Reproduce

1. **Download** the dataset from Kaggle and place the CSVs in `data/raw/`. Create `data/processed/`.
2. **Install dependencies:** `pip install pandas sqlalchemy psycopg2-binary`
3. **Create a PostgreSQL database**, e.g. `retail_analytics`.
4. **Set the connection string** as an environment variable (never hardcode credentials):
   ```bash
   export DATABASE_URL="postgresql://<user>:<password>@localhost:5432/retail_analytics"
   ```
5. **Run the scripts** from the `scripts/` folder: first the cleaning script, then the loading script.
6. **Run** `sql/create_analytical_model.sql` to build the star schema, then the analysis queries.
7. **Open** `olist_analytics_dashboard.pbix` in Power BI Desktop and point it to your database.
