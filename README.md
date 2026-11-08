# Loan Collection Management System

## Overview

A Python and MySQL-based Loan Collection Management System that processes loan, EMI, payment, delinquency, risk, and collection data.

The project demonstrates data processing, collection prioritization, customer contact restrictions, Promise-to-Pay tracking, database integration, data validation, and interactive dashboard reporting.

It includes a Streamlit dashboard for monitoring loan portfolios, collection performance, delinquency, risk indicators, and payment commitments.

## Technology Stack

- Python 3.14
- MySQL
- mysql-connector-python
- Streamlit
- Pandas
- Plotly
- Faker
- CSV-based data processing
- SQL

## Key Features

1. **Loan and EMI Management** – Generates EMI schedules and tracks installment records.
2. **Payment Processing** – Processes payment records and reconciles paid and outstanding amounts.
3. **Delinquency Tracking** – Calculates Days Past Due (DPD) and loan-level outstanding balances.
4. **Risk Assessment** – Generates risk indicators based on repayment behaviour and configured test scenarios.
5. **Collection Prioritization** – Calculates collection priority scores and ranks loans.
6. **Collection Case Management** – Generates collection cases with appropriate action statuses.
7. **Contact Preferences** – Tracks customer communication preferences and restrictions.
8. **Contact Attempts** – Validates communication channels, permitted hours, and contact eligibility.
9. **Promise-to-Pay** – Tracks customer payment commitments, payment allocations, and remaining amounts.
10. **Database Integration** – Imports collection-related records into MySQL.
11. **Interactive Dashboard** – Displays loan portfolio metrics, collection performance, risk analysis, and Promise-to-Pay tracking using Streamlit and Plotly.

## Dashboard

The project includes an interactive dashboard built with Streamlit, Pandas, Plotly, and MySQL.

### Dashboard Features

- Loan portfolio overview
- Total collection cases
- Outstanding loan amount
- Average Days Past Due (DPD)
- Collection priority score visualization
- Risk score analysis
- Collection action status distribution
- Promise-to-Pay tracking
- Paid versus remaining promise amounts
- Customer and loan search
- Collection status filters

### Run the Dashboard

From the project root directory, execute:

```bash
python -m streamlit run dashboard.py
```

Open the local URL displayed in the terminal, normally:

```text
http://localhost:8501
```

Enter the MySQL connection details in the dashboard sidebar to load the data.

## Project Structure

```text
Loan_Collection_Management_System/
│
├── data/
│   ├── customers.csv
│   ├── loans.csv
│   ├── all_emi_schedules.csv
│   ├── payments.csv
│   ├── delinquency.csv
│   ├── risk_indicators.csv
│   ├── collection_priority.csv
│   ├── collection_cases.csv
│   ├── contact_preferences.csv
│   ├── contact_attempts.csv
│   ├── promises_to_pay.csv
│   └── promise_payment_allocations.csv
│
├── database/
│   └── schema.sql
│
├── src/
│   ├── business/
│   ├── database/
│   ├── generator/
│   └── validation/
│
├── dashboard.py
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/ramcharankalvala/Loan_Collection_Management_System-Copy.git

cd Loan_Collection_Management_System-Copy
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure MySQL

- Start your MySQL server.
- Open `database/schema.sql` in MySQL Workbench.
- Execute the SQL script.
- The script creates the `loan_collection_db` database and its 13 tables.
- Configure your local MySQL credentials through the database connection module or the dashboard sidebar.
- Do not commit database passwords or other credentials to GitHub.

## Running the Project

The implementation uses separate Python scripts for data generation, business processing, database imports, and validation.

Run the required scripts individually from the project root.

Examples of database import modules:

```bash
python -m src.database.import_collection_priority

python -m src.database.import_collection_cases

python -m src.database.import_contact_attempts
```

Other available import modules include:

- Contact preferences
- Risk indicators
- Promises to Pay
- Promise-payment allocations

### Launch the Dashboard

```bash
python -m streamlit run dashboard.py
```

## Validation

The project includes validation scripts for:

- EMI schedules
- Installment payments
- Delinquency summaries
- Collection cases
- Contact preferences
- Contact attempts
- Promises to Pay

The tested EMI, installment payment, collection case, contact attempt, and Promise-to-Pay validation modules completed successfully with zero reported validation errors.

## Sample Verified Results

The following results are based on the included demonstration dataset and its current MySQL records.

| Metric | Result |
|---|---:|
| Customers | 1,000 |
| Loans | 5 |
| EMI schedules | 60 |
| Payment records | 45 |
| Collection cases | 5 |
| Contact attempts | 6 |
| Promises to Pay | 5 |
| Total promised | 50,000.00 |
| Total paid | 25,769.76 |
| Total remaining | 24,230.24 |

### Promise-to-Pay Reconciliation

```text
Total Promised = Total Paid + Total Remaining

50,000.00 = 25,769.76 + 24,230.24
```

The Promise-to-Pay amounts reconcile with the current test dataset.

## Notes and Limitations

- The included dataset is synthetic and intended for demonstration and testing.
- Some calculations use fixed reference dates to make test results reproducible.
- Risk and hardship scenarios are configured test scenarios, not predictions from a trained machine-learning model.
- The project currently uses Python scripts and a Streamlit dashboard.
- A REST API and live customer communication integration are not included.
- `main.py` currently displays a project menu; it is not an end-to-end workflow runner.

## Author

**Ramcharan Teja**

Python | SQL | MySQL | Java | Streamlit