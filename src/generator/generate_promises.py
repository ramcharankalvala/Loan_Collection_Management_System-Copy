
import csv
from datetime import date

# Step 1: Load existing loan records
with open("data/loans.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    loans = list(reader)

print("Total loans loaded:", len(loans))

# Step 2: Fixed reference date
reference_date = date(2026, 11, 20)

# Step 3: Sample promise amounts
promise_amounts = [10000, 15000, 8000, 5000, 12000]

# Step 4: Sample promise dates
promise_dates = [
    "2026-11-15",
    "2026-11-15",
    "2026-11-15",
    "2026-11-25",
    "2026-11-18"
]

# Step 5: Generate promises
promises = []

for i, loan in enumerate(loans, start=1):

    promise_amount = promise_amounts[i - 1]
    promise_date = promise_dates[i - 1]

    # Actual payments will be calculated
    # later from payment allocations
    amount_paid = 0.00

    remaining_amount = promise_amount

    # Initial promise status
    if reference_date > date.fromisoformat(promise_date):
        promise_status = "MISSED"
    else:
        promise_status = "PENDING"

    promise = {
        "promise_id": f"PTP-{i:06d}",
        "loan_id": loan["loan_id"],
        "customer_id": loan["customer_id"],
        "promise_amount": promise_amount,
        "promise_date": promise_date,
        "created_date": "2026-11-08",
        "amount_paid": amount_paid,
        "remaining_amount": remaining_amount,
        "promise_status": promise_status
    }

    promises.append(promise)

# Step 6: Save promises
fieldnames = [
    "promise_id",
    "loan_id",
    "customer_id",
    "promise_amount",
    "promise_date",
    "created_date",
    "amount_paid",
    "remaining_amount",
    "promise_status"
]

with open("data/promises_to_pay.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(promises)

print("\nTotal promises generated:", len(promises))
print("Promise records saved successfully!")
