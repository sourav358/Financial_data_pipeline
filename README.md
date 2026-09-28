# Financial Data Pipeline & Dashboard

A Python-based financial data pipeline that collects, cleans, validates, and
visualizes financial data for Reliance Industries.

The project takes financial data from Screener.in and converts it into
structured CSV files that can be viewed through a simple web dashboard.

---

## Project Overview

The project follows a simple end-to-end pipeline:

```text
Screener.in
     ↓
Data Scraper
     ↓
Raw Data
     ↓
Data Cleaner
     ↓
Processed CSV Files
     ↓
Data Validator
     ↓
Validation Report
     ↓
Financial Dashboard
```

The main purpose of the project is to demonstrate how raw financial data can
be transformed into clean, validated, and usable financial information.

---

## What I Built

- Scraped consolidated financial data from Screener.in
- Stored raw scraped data separately
- Cleaned and standardized the extracted tables
- Generated structured CSV datasets
- Added data-quality checks
- Added financial calculation checks
- Added OPM validation
- Added external validation against reference figures
- Generated a validation report
- Built a web dashboard to display the financial data
- Displayed validation results directly on the dashboard

---

## Project Structure

```text
Financial_data_pipeline/
│
├── scraper/
│   └── scraper.py
│
├── cleaning/
│   └── cleaner.py
│
├── validation/
│   └── validator.py
│
├── data/
│   ├── raw/
│   │   ├── screener_*.html
│   │   └── screener_tables_*.json
│   │
│   ├── processed/
│   │   ├── profit_loss.csv
│   │   ├── balance_sheet.csv
│   │   ├── cash_flow.csv
│   │   ├── ratios.csv
│   │   └── quarterly_results.csv
│   │
│   └── validation_report.csv
│
├── dashboard/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

# How to Run

## 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Financial_data_pipeline
```

Replace `<YOUR_GITHUB_REPOSITORY_URL>` with your GitHub repository URL.

---

## 2. Create a Virtual Environment

On Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Run the Complete Pipeline

From the project root:

```bash
python main.py


## 5. Start the Dashboard

From the project root:

```bash
python -m http.server 8000
```

Open the following URL in your browser:

```text
http://localhost:8000/dashboard/
```

The dashboard will load the processed CSV files and display the financial
data.

---

# Quick Start

If the environment has already been configured:

```bash
python main.py
python -m http.server 8000
```

Then open:

```text
http://localhost:8000/dashboard/
```

 

 

 

 
 