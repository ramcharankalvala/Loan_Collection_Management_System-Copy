
import csv
from datetime import date

# Step 1: Load EMI installment records
with open("data/all_emi_schedules.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    installments = list(reader)

print("Total installments:", len(installments))


# Step 2: Load actual payment records
with open("data/payments.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    payments = list(reader)

print("Total payment records:", len(payments))


# Step 3: Create payment lookup dictionary
payment_lookup = {}

for payment in payments:

    key = (payment["loan_id"], payment["installment_number"])

    payment_lookup[key] = payment

print("Payment lookup entries:", len(payment_lookup))


# Step 4: Set reference date
today = date(2026, 12, 31)


# Step 5: Calculate delinquency for every installment
delinquency_records = []

for installment in installments:

    loan_id = installment["loan_id"]
    customer_id = installment["customer_id"]
    installment_number = installment["month"]

    emi_amount = float(installment["emi"])

    due_date = date.fromisoformat(installment["due_date"])

    # Find the matching payment
    key = (loan_id, installment_number)

    if key in payment_lookup:
        amount_paid = float(payment_lookup[key]["amount_paid"])
    else:
        amount_paid = 0

    # Calculate outstanding amount
    outstanding_amount = round(emi_amount - amount_paid, 2)

    # Calculate DPD
    if today > due_date and outstanding_amount > 0:
        dpd = (today - due_date).days
    else:
        dpd = 0

    # Determine installment status
    if outstanding_amount == 0:
        status = "PAID"
    elif amount_paid > 0:
        status = "PARTIAL"
    elif dpd > 0:
        status = "MISSED"
    else:
        status = "NOT_DUE"

    # Create delinquency record
    record = {
        "loan_id": loan_id,
        "customer_id": customer_id,
        "installment_number": installment_number,
        "due_date": due_date.isoformat(),
        "emi_amount": emi_amount,
        "amount_paid": amount_paid,
        "outstanding_amount": outstanding_amount,
        "days_past_due": dpd,
        "installment_status": status
    }

    delinquency_records.append(record)


# Step 6: Count installment statuses
paid_count = 0
partial_count = 0
missed_count = 0
not_due_count = 0

for record in delinquency_records:

    if record["installment_status"] == "PAID":
        paid_count += 1

    elif record["installment_status"] == "PARTIAL":
        partial_count += 1

    elif record["installment_status"] == "MISSED":
        missed_count += 1

    elif record["installment_status"] == "NOT_DUE":
        not_due_count += 1


# Step 7: Calculate total amounts
total_emi_amount = 0
total_paid = 0
total_outstanding = 0

for record in delinquency_records:

    total_emi_amount += record["emi_amount"]
    total_paid += record["amount_paid"]
    total_outstanding += record["outstanding_amount"]

total_emi_amount = round(total_emi_amount, 2)
total_paid = round(total_paid, 2)
total_outstanding = round(total_outstanding, 2)


# Step 8: Save delinquency records
with open("data/delinquency.csv", "w", newline="", encoding="utf-8") as file:

    fieldnames = [
        "loan_id",
        "customer_id",
        "installment_number",
        "due_date",
        "emi_amount",
        "amount_paid",
        "outstanding_amount",
        "days_past_due",
        "installment_status"
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(delinquency_records)


# Step 9: Display summary
print("\n---------- DELINQUENCY SUMMARY ----------")

print("Total installments:", len(delinquency_records))
print("Fully paid installments:", paid_count)
print("Partially paid installments:", partial_count)
print("Missed installments:", missed_count)
print("Not yet due installments:", not_due_count)

print("\nTotal EMI amount:", total_emi_amount)
print("Total amount paid:", total_paid)
print("Total outstanding amount:", total_outstanding)

print("\nDelinquency records saved successfully!")
