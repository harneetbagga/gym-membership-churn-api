# 🏋️ Gym Membership Churn – End‑to‑End Analytics & FastAPI Backend

## Overview

This project demonstrates an **end‑to‑end data engineering and backend API workflow** built around a real‑world business problem: **gym membership churn analysis**.

The project is intentionally split into two clear phases:

1. **Offline analytics & feature engineering** to understand churn drivers
2. **Production‑style data API** to serve cleaned data and aggregated insights

It is designed as a **portfolio‑ready project** that mirrors how data engineers and backend developers structure analytical systems in real environments.

---

## Highlights

* End‑to‑end churn analysis from raw CSV to API‑ready data
* Feature engineering and exploratory data analysis (EDA)
* Clean separation between analytics and backend layers
* FastAPI backend with schema‑validated responses (Pydantic)
* DuckDB used as an analytical database
* SQL‑based aggregations and filters
* Pagination and query parameter validation
* Auto‑generated API documentation via Swagger UI

---

## Tech Stack

* **Python 3.x**
* **Pandas** – Data cleaning & EDA
* **Matplotlib** – Visualizations
* **Polars** – Fast CSV loading & transformation
* **FastAPI** – Backend API
* **Pydantic** – Schema validation
* **DuckDB** – Analytical SQL database
* **Uvicorn** – ASGI server

---

## Project Structure

```
gym-membership-churn-api/
│
├── analytics/
│   └── data_cleaning.py          # EDA & feature engineering
│
├── app/
│   ├── main.py                   # FastAPI application
│   └── schemas.py                # Pydantic models
│
├── data/
│   ├── gym_members_dataset.csv   # Source dataset
│   └── gym_members_dataset.duckdb# DuckDB analytical database
│
├── visualizations/
│   ├── age_histogram_plot.png
│   ├── membership_type.png
│   ├── workout_duration_comparison.png
│   └── gender_churn_distribution.png
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Phase 1: Analytics & Feature Engineering

**File:** `analytics/data_cleaning.py`

### Key Steps

* Removed invalid records (missing Member ID or Age)
* Standardized date columns (`Join_Date`, `Last_Visit_Date`)
* Filled missing values using business‑safe defaults
* Engineered new features:

  * `Membership_Period_Days`
  * `Days_Since_Last_Visit`

### Exploratory Analysis

The following visualizations are generated and saved to disk:

* Age distribution histogram
* Membership type distribution
* Average workout duration (Churned vs Active)
* Gender distribution split by churn

These insights help identify behavioral patterns related to churn **before** data is exposed via APIs.

---

## Phase 2: Backend API & Data Serving

**File:** `app/main.py`

### Data Pipeline

1. Load CSV using Polars
2. Apply cleaning rules
3. Persist data to DuckDB
4. Serve data through FastAPI endpoints

### API Endpoints

#### 1️⃣ Serve Raw Dataset

```
GET /serving_raw_dataset
```

Returns the cleaned dataset as JSON.

---

#### 2️⃣ Churn Count by Membership Type

```
GET /churn_by_membership_count
```

Returns aggregated churn counts using SQL.

---

#### 3️⃣ Filter by Favorite Exercise

```
GET /favorite-exercise-member-count?exercise=Squats
```

Uses query parameters with validation and parameterized SQL.

---

#### 4️⃣ Pagination Endpoint

```
GET /data-using-pagination?page=2&page_size=5
```

Returns paginated member records with metadata:

* total records
* page number
* page size

---

## Schema Validation

**File:** `app/schemas.py`

Pydantic models enforce:

* Strong typing
* Consistent API responses
* Improved Swagger documentation

This prevents malformed data from reaching API consumers.

---

## How to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/gym-membership-churn-api.git
cd gym-membership-churn-api
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the API

```bash
python app/main.py
```

### 5. Open Swagger UI

```
http://localhost:8080/docs
```

---

## Why DuckDB?

DuckDB provides:

* Embedded analytical SQL engine
* No external server dependency
* Excellent performance for analytical queries

This makes it ideal for backend analytics APIs and local data services.

---

## Production & Scalability Considerations

* Separation of analytics and serving layers
* SQL‑based aggregations for performance
* Pagination for large datasets
* Schema validation to protect consumers
* Easily extendable to Airflow, Docker, or cloud deployment

---

## Disclaimer

The dataset used is publicly available and intended for educational purposes. This project is for learning and portfolio demonstration only.

---

## Author

**Harneet Bagga**
Senior QA & Data Engineering Professional
