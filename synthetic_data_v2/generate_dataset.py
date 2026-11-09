import csv
import json
import random
import hashlib
from pathlib import Path
from datetime import date, datetime, timedelta
from faker import Faker

# =========================================================
# LOAN COLLECTION MANAGEMENT SYSTEM
# Synthetic Dataset Generator - Version 2
# =========================================================

SEED = 20261022
TOTAL_LOANS = 10000
INSTALLMENTS_PER_LOAN = 3
AS_OF_DATE = date(2026, 12, 31)

random.seed(SEED)
fake = Faker("en_IN")
fake.seed_instance(SEED)

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def write_csv(filename, rows):
    """Write a list of dictionaries to a CSV file."""
    if not rows:
        return

    with open(OUTPUT_DIR / filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def money(value):
    return round(float(value), 2)


def make_id(prefix, number):
    return f"{prefix}-2026-{number:06d}"


# =========================================================
# 1. CUSTOMERS
# =========================================================

customers = []

for i in range(1, TOTAL_LOANS + 1):
    customers.append({
        "customer_id": f"CUST-{i:06d}",
        "name": fake.name(),
        "email": f"customer{i}@example.com",
        "city": fake.city(),
        "phone": f"9{random.randint(100000000, 999999999)}"
    })


# =========================================================
# 2. ACCOUNTS AND LOANS
# =========================================================

accounts = []
loans = []

loan_amount_choices = [50000, 75000, 100000, 150000, 200000]

for i in range(1, TOTAL_LOANS + 1):
    customer_id = f"CUST-{i:06d}"
    account_id = f"ACC-2026-{i:06d}"
    loan_id = make_id("LOAN", i)

    principal = random.choice(loan_amount_choices)

    loans.append({
        "loan_id": loan_id,
        "account_id": account_id,
        "customer_id": customer_id,
        "loan_amount": principal,
        "annual_interest_rate": 12,
        "loan_date": "2025-12-01",
        "maturity_date": "2026-12-05"
    })

    accounts.append({
        "account_id": account_id,
        "customer_id": customer_id,
        "account_status": "ACTIVE",
        "opened_date": "2025-12-01",
        "closed_date": ""
    })


# =========================================================
# 3. INSTALLMENTS
# Exactly 3 installments per loan = 30,000 rows
# Due dates are distributed across a 12-month period.
# =========================================================

installments = []
installment_lookup = {}

due_months = [1, 6, 12]

for loan in loans:
    loan_id = loan["loan_id"]
    principal = loan["loan_amount"]
    customer_id = loan["customer_id"]

    installment_amount = money(principal / INSTALLMENTS_PER_LOAN)

    for number, month in enumerate(due_months, start=1):
        installment_id = f"INS-{loan_id}-{number:03d}"

        amount = installment_amount

        # Adjust the final installment to reconcile the total.
        if number == INSTALLMENTS_PER_LOAN:
            amount = money(principal - installment_amount * 2)

        row = {
            "installment_id": installment_id,
            "loan_id": loan_id,
            "customer_id": customer_id,
            "installment_number": number,
            "due_date": f"2026-{month:02d}-05",
            "installment_amount": amount
        }

        installments.append(row)
        installment_lookup[installment_id] = row


# =========================================================
# 4. PAYMENTS
# =========================================================

payments = []
payment_number = 1
installment_paid = {}

for installment in installments:
    loan_id = installment["loan_id"]
    customer_id = installment["customer_id"]
    installment_id = installment["installment_id"]
    installment_number = installment["installment_number"]
    amount_due = installment["installment_amount"]

    # Loan 1 is deliberately fully paid.
    if loan_id == "LOAN-2026-000001":
        payment_type = "FULL"
    else:
        payment_type = random.choices(
            ["FULL", "PARTIAL", "MISSED"],
            weights=[55, 25, 20],
            k=1
        )[0]

    amount_paid = 0

    if payment_type == "FULL":
        amount_paid = amount_due
    elif payment_type == "PARTIAL":
        amount_paid = money(amount_due * random.uniform(0.40, 0.80))

    installment_paid[installment_id] = amount_paid

    if amount_paid > 0:
        due_date = date.fromisoformat(installment["due_date"])
        payment_date = due_date + timedelta(days=random.randint(0, 10))

        payments.append({
            "payment_id": make_id("PMT", payment_number),
            "loan_id": loan_id,
            "customer_id": customer_id,
            "installment_id": installment_id,
            "installment_number": installment_number,
            "payment_date": payment_date.isoformat(),
            "amount_due": amount_due,
            "amount_paid": money(amount_paid),
            "payment_status": payment_type
        })

        payment_number += 1


# =========================================================
# 5. DELINQUENCY SNAPSHOTS
# =========================================================

delinquency = []

loan_totals = {}

for installment in installments:
    installment_id = installment["installment_id"]
    loan_id = installment["loan_id"]

    amount_due = installment["installment_amount"]
    amount_paid = installment_paid[installment_id]
    outstanding = money(amount_due - amount_paid)

    due_date = date.fromisoformat(installment["due_date"])

    if outstanding == 0:
        dpd = 0
        status = "PAID"
    elif AS_OF_DATE > due_date:
        dpd = (AS_OF_DATE - due_date).days
        status = "PARTIAL" if amount_paid > 0 else "MISSED"
    else:
        dpd = 0
        status = "DUE"

    delinquency.append({
        "snapshot_id": f"SNAP-{len(delinquency) + 1:06d}",
        "loan_id": loan_id,
        "installment_id": installment_id,
        "as_of_date": AS_OF_DATE.isoformat(),
        "due_date": due_date.isoformat(),
        "amount_due": amount_due,
        "amount_paid": money(amount_paid),
        "outstanding_amount": outstanding,
        "days_past_due": dpd,
        "installment_status": status
    })

    if loan_id not in loan_totals:
        loan_totals[loan_id] = {
            "total_due": 0,
            "total_paid": 0,
            "outstanding": 0,
            "max_dpd": 0,
            "missed_installments": 0
        }

    loan_totals[loan_id]["total_due"] += amount_due
    loan_totals[loan_id]["total_paid"] += amount_paid
    loan_totals[loan_id]["outstanding"] += outstanding
    loan_totals[loan_id]["max_dpd"] = max(
        loan_totals[loan_id]["max_dpd"], dpd
    )

    if status == "MISSED":
        loan_totals[loan_id]["missed_installments"] += 1


# =========================================================
# 6. CONTACT PREFERENCES
# =========================================================

contact_preferences = []

for i in range(1, TOTAL_LOANS + 1):
    opt_out = random.random() < 0.05

    contact_preferences.append({
        "customer_id": f"CUST-{i:06d}",
        "phone_allowed": not opt_out,
        "sms_allowed": not opt_out,
        "email_allowed": not opt_out,
        "contact_opt_out": opt_out,
        "allowed_start_time": "09:00",
        "allowed_end_time": "18:00"
    })


preference_lookup = {
    row["customer_id"]: row for row in contact_preferences
}


# =========================================================
# 7. COLLECTION CASES AND RISK INDICATORS
# =========================================================

collection_cases = []
risk_indicators = []

case_number = 1

for loan in loans:
    loan_id = loan["loan_id"]
    customer_id = loan["customer_id"]
    totals = loan_totals[loan_id]

    outstanding = money(totals["outstanding"])
    dpd = totals["max_dpd"]
    missed = totals["missed_installments"]

    hardship = random.random() < 0.08
    disputed = random.random() < 0.05
    contact_restricted = preference_lookup[customer_id]["contact_opt_out"]

    risk_score = min(
        100,
        missed * 15
        + (20 if dpd > 90 else 10 if dpd > 30 else 0)
        + (15 if hardship else 0)
        + (15 if disputed else 0)
    )

    risk_indicators.append({
        "loan_id": loan_id,
        "missed_installments": missed,
        "days_past_due": dpd,
        "hardship_flag": hardship,
        "dispute_flag": disputed,
        "contact_restricted": contact_restricted,
        "risk_score": risk_score
    })

    # Only loans with outstanding balances enter normal collection.
    if outstanding > 0:
        priority_score = min(
            100,
            int(risk_score + min(outstanding / 5000, 40))
        )

        collection_cases.append({
            "case_id": make_id("COL", case_number),
            "loan_id": loan_id,
            "account_id": loan["account_id"],
            "customer_id": customer_id,
            "outstanding": outstanding,
            "days_past_due": dpd,
            "risk_score": risk_score,
            "priority_score": priority_score,
            "priority_rank": 0,
            "case_status": "OPEN",
            "action_status": "REVIEW_REQUIRED",
            "dispute_status": "DISPUTED" if disputed else "NO_DISPUTE",
            "hardship_status": "HARDSHIP" if hardship else "NO_HARDSHIP",
            "contact_status": "RESTRICTED" if contact_restricted else "ALLOWED"
        })

        case_number += 1


# Rank cases by priority score.
collection_cases.sort(
    key=lambda x: x["priority_score"],
    reverse=True
)

for rank, case in enumerate(collection_cases, start=1):
    case["priority_rank"] = rank


# =========================================================
# 8. CONTACT ATTEMPTS
# =========================================================

contact_attempts = []

for case in collection_cases:
    customer_id = case["customer_id"]
    preference = preference_lookup[customer_id]

    if preference["contact_opt_out"]:
        continue

    case_id = case["case_id"]

    contact_attempts.append({
        "attempt_id": f"CTP-{case_id}-001",
        "case_id": case_id,
        "loan_id": case["loan_id"],
        "customer_id": customer_id,
        "attempt_datetime": "2026-12-15 11:00:00",
        "channel": random.choice(["PHONE", "SMS", "EMAIL"]),
        "outcome": random.choice([
            "NO_ANSWER", "CONNECTED", "CALL_BACK_REQUESTED"
        ]),
        "within_allowed_window": True
    })


# =========================================================
# 9. PROMISES TO PAY
# =========================================================

promises = []
promise_number = 1

for case in collection_cases:
    if random.random() > 0.15:
        continue

    arrears = case["outstanding"]

    if arrears <= 0:
        continue

    promise_amount = money(
        arrears * random.uniform(0.20, 0.80)
    )

    promises.append({
        "promise_id": make_id("PTP", promise_number),
        "case_id": case["case_id"],
        "loan_id": case["loan_id"],
        "customer_id": case["customer_id"],
        "promise_amount": promise_amount,
        "created_date": "2026-12-15",
        "promise_date": "2027-01-05",
        "amount_paid": 0,
        "remaining_amount": promise_amount,
        "promise_status": "OPEN"
    })

    promise_number += 1


# =========================================================
# 10. INJECT LABELLED EDGE CASES
# These are deliberate anomalies, not normal baseline records.
# Labels are stored separately in ground_truth.csv.
# =========================================================

ground_truth = []


def add_ground_truth(record_id, entity, anomaly, expected_decision):
    ground_truth.append({
        "record_id": record_id,
        "entity": entity,
        "anomaly_type": anomaly,
        "expected_decision": expected_decision
    })


# Edge case 1: Paid-off account remains in collection.
paid_loan = loans[0]

paid_case = {
    "case_id": make_id("COL", case_number),
    "loan_id": paid_loan["loan_id"],
    "account_id": paid_loan["account_id"],
    "customer_id": paid_loan["customer_id"],
    "outstanding": 0,
    "days_past_due": 0,
    "risk_score": 0,
    "priority_score": 90,
    "priority_rank": 0,
    "case_status": "OPEN",
    "action_status": "COLLECTION_REQUIRED",
    "dispute_status": "NO_DISPUTE",
    "hardship_status": "NO_HARDSHIP",
    "contact_status": "ALLOWED"
}

collection_cases.append(paid_case)

add_ground_truth(
    paid_case["case_id"],
    "CollectionCase",
    "PAID_ACCOUNT_IN_COLLECTION",
    "REMOVE_FROM_COLLECTION"
)

# Mark the account as paid off.
accounts[0]["account_status"] = "PAID_OFF"
accounts[0]["closed_date"] = "2026-12-31"


# Edge case 2: Contact attempt outside permitted time window.
if contact_attempts:
    contact_attempts[0]["attempt_datetime"] = "2026-12-15 22:30:00"
    contact_attempts[0]["within_allowed_window"] = False

    add_ground_truth(
        contact_attempts[0]["attempt_id"],
        "ContactAttempt",
        "CONTACT_OUTSIDE_ALLOWED_WINDOW",
        "FLAG_AND_BLOCK_CONTACT"
    )


# Edge case 3: Payment allocated to the wrong installment.
if payments:
    wrong_payment = payments[0]
    original_installment_id = wrong_payment["installment_id"]

    other_installment = installments[-1]

    if other_installment["loan_id"] == wrong_payment["loan_id"]:
        other_installment = installments[-2]

    wrong_payment["installment_id"] = other_installment["installment_id"]

    add_ground_truth(
        wrong_payment["payment_id"],
        "Payment",
        "WRONG_INSTALLMENT_ALLOCATION",
        "REJECT_AND_REALLOCATE_PAYMENT"
    )


# Edge case 4: Promise amount exceeds arrears.
if collection_cases:
    target_case = collection_cases[0]
    excessive_amount = money(target_case["outstanding"] + 1000)

    excessive_promise = {
        "promise_id": make_id("PTP", promise_number),
        "case_id": target_case["case_id"],
        "loan_id": target_case["loan_id"],
        "customer_id": target_case["customer_id"],
        "promise_amount": excessive_amount,
        "created_date": "2026-12-20",
        "promise_date": "2027-01-10",
        "amount_paid": 0,
        "remaining_amount": excessive_amount,
        "promise_status": "OPEN"
    }

    promises.append(excessive_promise)

    add_ground_truth(
        excessive_promise["promise_id"],
        "PromiseToPay",
        "PROMISE_EXCEEDS_ARREARS",
        "FLAG_FOR_REVIEW"
    )


# Edge case 5: Disputed debt treated as confirmed.
if collection_cases:
    disputed_case = collection_cases[1] if len(collection_cases) > 1 else collection_cases[0]

    disputed_case["dispute_status"] = "DISPUTED"
    disputed_case["action_status"] = "COLLECTION_CONFIRMED"

    add_ground_truth(
        disputed_case["case_id"],
        "CollectionCase",
        "DISPUTED_DEBT_TREATED_AS_CONFIRMED",
        "HOLD_FOR_DISPUTE_REVIEW"
    )


# Recalculate ranks after anomaly injection.
collection_cases.sort(
    key=lambda x: x["priority_score"],
    reverse=True
)

for rank, case in enumerate(collection_cases, start=1):
    case["priority_rank"] = rank


# =========================================================
# 11. VALIDATION
# =========================================================

errors = []

def check_unique(rows, key, name):
    values = [row[key] for row in rows]

    if len(values) != len(set(values)):
        errors.append(f"Duplicate primary keys found in {name}")


check_unique(customers, "customer_id", "customers")
check_unique(accounts, "account_id", "accounts")
check_unique(loans, "loan_id", "loans")
check_unique(installments, "installment_id", "installments")
check_unique(payments, "payment_id", "payments")
check_unique(collection_cases, "case_id", "collection_cases")
check_unique(promises, "promise_id", "promises")

if len(loans) != TOTAL_LOANS:
    errors.append("Loan count is incorrect")

if len(installments) != TOTAL_LOANS * INSTALLMENTS_PER_LOAN:
    errors.append("Installment count is incorrect")

customer_ids = {x["customer_id"] for x in customers}
loan_ids = {x["loan_id"] for x in loans}
installment_ids = {x["installment_id"] for x in installments}

for loan in loans:
    if loan["customer_id"] not in customer_ids:
        errors.append("Invalid customer foreign key in loans")
        break

for installment in installments:
    if installment["loan_id"] not in loan_ids:
        errors.append("Invalid loan foreign key in installments")
        break

for payment in payments:
    if payment["loan_id"] not in loan_ids:
        errors.append("Invalid loan foreign key in payments")
        break

    if payment["installment_id"] not in installment_ids:
        errors.append("Invalid installment foreign key in payments")
        break

if not ground_truth or len(ground_truth) != 5:
    errors.append("Expected exactly five labelled edge cases")


# =========================================================
# 12. EXPORT CSV FILES
# =========================================================

datasets = {
    "customers.csv": customers,
    "accounts.csv": accounts,
    "loans.csv": loans,
    "installments.csv": installments,
    "payments.csv": payments,
    "delinquency_snapshots.csv": delinquency,
    "contact_preferences.csv": contact_preferences,
    "contact_attempts.csv": contact_attempts,
    "promises_to_pay.csv": promises,
    "collection_cases.csv": collection_cases,
    "risk_indicators.csv": risk_indicators,
    "ground_truth.csv": ground_truth
}

for filename, rows in datasets.items():
    write_csv(filename, rows)


# =========================================================
# 13. DATA SUMMARY AND CHECKSUMS
# =========================================================

summary = {}

checksums = {}

for filename, rows in datasets.items():
    summary[filename] = len(rows)

    file_path = OUTPUT_DIR / filename

    with open(file_path, "rb") as file:
        checksums[filename] = hashlib.sha256(
            file.read()
        ).hexdigest()


with open(OUTPUT_DIR / "validation_summary.json", "w", encoding="utf-8") as file:
    json.dump({
        "seed": SEED,
        "as_of_date": AS_OF_DATE.isoformat(),
        "validation_status": "PASSED" if not errors else "FAILED",
        "errors": errors,
        "row_counts": summary
    }, file, indent=4)


with open(OUTPUT_DIR / "checksums.json", "w", encoding="utf-8") as file:
    json.dump(checksums, file, indent=4)


with open(OUTPUT_DIR / "source_manifest.json", "w", encoding="utf-8") as file:
    json.dump({
        "generator": "generate_dataset.py",
        "version": "2.0",
        "seed": SEED,
        "loan_count": TOTAL_LOANS,
        "installments_per_loan": INSTALLMENTS_PER_LOAN,
        "total_installments": len(installments),
        "as_of_date": AS_OF_DATE.isoformat(),
        "notes": "Synthetic data generated for a loan collection management challenge."
    }, file, indent=4)


# =========================================================
# 14. FINAL RESULT
# =========================================================

print("\n========== DATA GENERATION COMPLETE ==========")

for filename, count in summary.items():
    print(f"{filename:<32} {count:>10,} rows")

print("\nTotal loans:", len(loans))
print("Total installments:", len(installments))
print("Total payments:", len(payments))
print("Ground-truth anomalies:", len(ground_truth))

if errors:
    print("\nVALIDATION FAILED")
    for error in errors:
        print("-", error)
else:
    print("\nVALIDATION PASSED")

print("\nOutput folder:", OUTPUT_DIR)