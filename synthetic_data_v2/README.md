\# Loan Collection Management System – Synthetic Dataset V2



\## 1. Project Overview



This project generates a deterministic synthetic loan collection dataset for testing, analysis, collection prioritization, delinquency monitoring, and data-quality validation.



The dataset simulates a loan portfolio with customers, accounts, loans, installments, payments, delinquency snapshots, contact preferences, collection cases, risk indicators, contact attempts, and promises to pay.



It also includes five deliberately injected edge cases with a separate ground-truth file for validation.



\## 2. Technology Stack



\- Python

\- Faker

\- CSV data processing

\- JSON metadata and validation reports

\- MySQL-compatible SQL export (generated separately)



\## 3. Dataset Size



Generated using a fixed random seed: `20261022`.



| Dataset | Records |

|---|---:|

| Customers | 10,000 |

| Accounts | 10,000 |

| Loans | 10,000 |

| Installments | 30,000 |

| Payments | 23,944 |

| Delinquency snapshots | 30,000 |

| Contact preferences | 10,000 |

| Contact attempts | 7,950 |

| Promises to pay | 1,246 |

| Collection cases | 8,390 |

| Risk indicators | 10,000 |

| Ground-truth anomalies | 5 |



Each loan has three installments. Their due dates are distributed across January, June, and December 2026, providing a 12-month reference period and a total of 30,000 installment records.



\## 4. Project Structure



```text

Loan\_Collection\_Management\_System/

│

├── dashboard.py

├── main.py

├── src/

│   ├── business/

│   ├── database/

│   ├── generator/

│   └── validation/

│

└── synthetic\_data\_v2/

&#x20;   ├── generate\_dataset.py

&#x20;   ├── README.md

&#x20;   ├── data\_dictionary.md

&#x20;   └── output/

&#x20;       ├── customers.csv

&#x20;       ├── accounts.csv

&#x20;       ├── loans.csv

&#x20;       ├── installments.csv

&#x20;       ├── payments.csv

&#x20;       ├── delinquency\_snapshots.csv

&#x20;       ├── contact\_preferences.csv

&#x20;       ├── contact\_attempts.csv

&#x20;       ├── promises\_to\_pay.csv

&#x20;       ├── collection\_cases.csv

&#x20;       ├── risk\_indicators.csv

&#x20;       ├── ground\_truth.csv

&#x20;       ├── validation\_summary.json

&#x20;       ├── checksums.json

&#x20;       └── source\_manifest.json

```



SQL export files will be generated separately in the output directory.



\## 5. Dataset Generation



\### Prerequisites



\- Python 3.10 or later

\- Faker package



Install Faker if it is not already installed:



```powershell

python -m pip install Faker

```



\### Generate the dataset



Run from the project root:



```powershell

python synthetic\_data\_v2\\generate\_dataset.py

```



Generated files are written to:



```text

synthetic\_data\_v2/output/

```



\### Reproducibility



The generator uses a fixed random seed:



```python

SEED = 20261022

```



Running the generator again with the same configuration produces the same dataset and checksums.



\## 6. Data Model



The dataset follows a parent-to-child structure:



1\. Customers

2\. Accounts

3\. Loans

4\. Installments

5\. Payments

6\. Delinquency snapshots

7\. Collection cases

8\. Risk indicators

9\. Contact preferences

10\. Contact attempts

11\. Promises to pay

12\. Ground truth



Primary keys use deterministic identifiers with zero-padded sequence numbers. Child records reference their corresponding parent identifiers.



Refer to `data\_dictionary.md` for field definitions, data types, and validation rules.



\## 7. Business Scenarios



The generated dataset supports analysis of:



\- Outstanding loan balances

\- Installment payment status

\- Days past due (DPD)

\- Partial and missed payments

\- Collection case prioritization

\- Customer contact restrictions

\- Hardship and dispute scenarios

\- Promise-to-pay tracking

\- Payment reconciliation

\- Portfolio risk monitoring



Priority scores and risk indicators are synthetic rule-based values, not outputs from a trained machine-learning model.



\## 8. Injected Edge Cases



Five labelled anomalies are deliberately included:



| Scenario | Expected Decision |

|---|---|

| Paid-off account remains in collection | Remove from collection |

| Contact outside permitted window | Flag and block contact |

| Payment allocated to wrong installment | Reject and reallocate payment |

| Promise exceeds arrears | Flag for review |

| Disputed debt treated as confirmed | Hold for dispute review |



The labels are stored in `ground\_truth.csv`. This file must remain separate from operational features to prevent data leakage.



\## 9. Validation and Quality Checks



The generator checks:



\- Primary-key uniqueness

\- Required parent-record references

\- Expected loan and installment counts

\- Loan principal reconciliation

\- Payment amount validity

\- Delinquency balance arithmetic

\- Expected number of labelled anomalies

\- Dataset reproducibility through checksums



The generated dataset passed the generator's built-in validation.



An additional financial reconciliation check found:



\- Loan principal reconciliation errors: 0

\- Invalid payment amount records: 0

\- Delinquency arithmetic errors: 0

\- Installment payment mismatches: 2



The two installment mismatches are expected because one payment is deliberately allocated to another loan's installment. Both affected installment aggregates are therefore inconsistent and should be detected by downstream validation.



\## 10. Important Design Decisions and Limitations



\- All records are synthetic and do not represent real customers.

\- The generator uses a fixed reference date of December 31, 2026.

\- Three installments are generated per loan to meet the 30,000-installment target for 10,000 loans.

\- Collection priority and risk scores are rule-based synthetic values.

\- Five deliberate anomalies are included for testing.

\- Ground-truth labels are kept separate from operational data.

\- The generator's built-in checks do not replace every possible cross-table business validation.



\## 11. Reproducibility Verification



The generator was executed repeatedly with the same seed. The resulting checksums were compared, and no differences were reported.



This confirms that the generated files are reproducible with the current generator and configuration.



\## 12. Output Files



The `output` directory contains:



\- CSV files for the generated entities

\- `ground\_truth.csv` for labelled anomalies

\- `validation\_summary.json` for validation information

\- `checksums.json` for reproducibility checks

\- `source\_manifest.json` for dataset source and generation metadata

\- SQL schema and seed-data exports (generated separately)



\## 13. Running the Project



Generate the synthetic dataset:



```powershell

python synthetic\_data\_v2\\generate\_dataset.py

```



Run the existing Streamlit dashboard from the project root:



```powershell

python -m streamlit run dashboard.py

```



The dashboard and original project modules are maintained separately from the V2 synthetic dataset generator.

