
import csv
from collections import defaultdict
from datetime import date

# Step 1: Load promise records
with open("data/promises_to_pay.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    promises = list(reader)

print("Total promises loaded:", len(promises))

# Step 2: Load actual payment records
with open("data/payments.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    payments = list(reader)

print("Total payments loaded:", len(payments))

# Step 3: Group payments by loan ID
payments_by_loan = defaultdict(list)

for payment in payments:
    loan_id = payment["loan_id"]
    payments_by_loan[loan_id].append(payment)

# Step 4: Track unallocated payment amounts
payment_remaining = {}

for payment in payments:
    payment_id = payment["payment_id"]

    payment_remaining[payment_id] = round(
        float(payment["amount_paid"]), 2
    )

# Step 5: Track allocated amount for each promise
promise_paid = {
    promise["promise_id"]: 0.00
    for promise in promises
}

allocations = []
allocation_number = 1

# Step 6: Allocate eligible payments
for promise in promises:

    promise_id = promise["promise_id"]
    loan_id = promise["loan_id"]

    promise_amount = round(
        float(promise["promise_amount"]), 2
    )

    created_date = date.fromisoformat(promise["created_date"])
    promise_date = date.fromisoformat(promise["promise_date"])

    remaining_promise = promise_amount

    matching_payments = payments_by_loan.get(loan_id, [])

    matching_payments.sort(
        key=lambda payment: date.fromisoformat(
            payment["payment_date"]
        )
    )

    print("\nPromise ID:", promise_id)

    for payment in matching_payments:

        payment_date = date.fromisoformat(payment["payment_date"])

        if not created_date <= payment_date <= promise_date:
            continue

        payment_id = payment["payment_id"]

        available_payment = payment_remaining[payment_id]

        if available_payment <= 0:
            continue

        allocated_amount = round(
            min(remaining_promise, available_payment), 2
        )

        if allocated_amount <= 0:
            break

        allocation = {
            "allocation_id": f"ALLOC-{allocation_number:06d}",
            "promise_id": promise_id,
            "payment_id": payment_id,
            "allocated_amount": allocated_amount,
            "allocation_date": payment["payment_date"]
        }

        allocations.append(allocation)

        remaining_promise = round(
            remaining_promise - allocated_amount, 2
        )

        payment_remaining[payment_id] = round(
            available_payment - allocated_amount, 2
        )

        promise_paid[promise_id] = round(
            promise_paid[promise_id] + allocated_amount, 2
        )

        allocation_number += 1

        print(payment_id, "- Allocated:", allocated_amount)

        if remaining_promise <= 0:
            break

# Step 7: Update promise payment details
reference_date = date(2026, 11, 20)

for promise in promises:

    promise_id = promise["promise_id"]

    promise_amount = round(
        float(promise["promise_amount"]), 2
    )

    amount_paid = promise_paid[promise_id]

    remaining_amount = round(
        promise_amount - amount_paid, 2
    )

    promise_date = date.fromisoformat(
        promise["promise_date"]
    )

    if remaining_amount == 0:
        promise_status = "FULFILLED"

    elif amount_paid > 0:
        promise_status = "PARTIALLY_FULFILLED"

    elif reference_date > promise_date:
        promise_status = "MISSED"

    else:
        promise_status = "PENDING"

    promise["amount_paid"] = f"{amount_paid:.2f}"
    promise["remaining_amount"] = f"{remaining_amount:.2f}"
    promise["promise_status"] = promise_status

# Step 8: Save updated promises
promise_fields = [
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
    writer = csv.DictWriter(file, fieldnames=promise_fields)
    writer.writeheader()
    writer.writerows(promises)

# Step 9: Save allocations
allocation_fields = [
    "allocation_id",
    "promise_id",
    "payment_id",
    "allocated_amount",
    "allocation_date"
]

with open("data/promise_payment_allocations.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=allocation_fields)
    writer.writeheader()
    writer.writerows(allocations)

# Step 10: Display final summary
print("\n---------- ALLOCATION SUMMARY ----------")

print("Total allocations created:", len(allocations))

total_allocated = round(
    sum(item["allocated_amount"] for item in allocations), 2
)

print("Total amount allocated:", total_allocated)

print("\n---------- PROMISE RECONCILIATION ----------")

for promise in promises:
    print(
        promise["promise_id"],
        "| Paid:", promise["amount_paid"],
        "| Remaining:", promise["remaining_amount"],
        "| Status:", promise["promise_status"]
    )

print("\nPromise and allocation records saved successfully!")
