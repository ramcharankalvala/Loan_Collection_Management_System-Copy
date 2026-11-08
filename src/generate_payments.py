
import random
import csv
from datetime import date, timedelta

# Step 1: Load installment records
installments = []

with open("data/all_emi_schedules.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for record in reader:
        installments.append(record)

print("Total installments loaded:", len(installments))

# Step 2: Set random seed for reproducible data
random.seed(20261022)

# Step 3: Generate payment records
payment_records = []

for installment in installments:

    emi_amount = float(installment["emi"])

    # Generate a synthetic payment date
    due_date = date.fromisoformat(installment["due_date"])

    payment_date = due_date + timedelta(days=random.randint(0, 10))

    # Generate a payment amount
    payment_amount = random.choice([
        emi_amount,
        round(emi_amount / 2, 2),
        0
    ])

    # Determine payment status
    if payment_amount == 0:
        payment_status = "MISSED"

    elif payment_amount < emi_amount:
        payment_status = "PARTIAL"

    else:
        payment_status = "PAID"

    # Calculate unpaid amount
    unpaid_amount = round(emi_amount - payment_amount, 2)

    # Store only actual payments
    if payment_amount > 0:

        payment_record = {
            "payment_id": f"PMT-{len(payment_records) + 1:06d}",
            "loan_id": installment["loan_id"],
            "customer_id": installment["customer_id"],
            "installment_number": installment["month"],
            "payment_date": payment_date.isoformat(),
            "emi_amount": emi_amount,
            "amount_paid": payment_amount,
            "unpaid_amount": unpaid_amount,
            "payment_status": payment_status
        }

        payment_records.append(payment_record)

# Step 4: Display payment summary
print("\nTotal actual payment records:", len(payment_records))

print("\nFirst payment record:")
if payment_records:
    print(payment_records[0])

# Step 5: Save payment records to CSV
fieldnames = [
    "payment_id",
    "loan_id",
    "customer_id",
    "installment_number",
    "payment_date",
    "emi_amount",
    "amount_paid",
    "unpaid_amount",
    "payment_status"
]

with open("data/payments.csv", "w", newline="", encoding="utf-8") as file:

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(payment_records)

print("\nPayment records saved successfully!")
