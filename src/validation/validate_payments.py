
import csv
from datetime import date, timedelta

# Step 1: Load payment records
payments = []

with open("data/payments.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    payments = list(reader)

print("Total payment records:", len(payments))

# Step 2: Display first payment
print("\nFirst payment:")

if payments:
    print(payments[0])

# Step 3: Check duplicate payment IDs
payment_ids = []

for payment in payments:
    payment_ids.append(payment["payment_id"])

duplicate_errors = len(payment_ids) - len(set(payment_ids))

if duplicate_errors == 0:
    print("\nNo duplicate payment IDs")
else:
    print("\nDuplicate payment IDs found")

# Step 4: Load original loan IDs
loan_ids = set()

with open("data/loans.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for loan in reader:
        loan_ids.add(loan["loan_id"])

# Step 5: Validate payment loan IDs
relationship_errors = 0

for payment in payments:

    if payment["loan_id"] not in loan_ids:
        print(
            payment["payment_id"],
            "- Loan ID does not exist:",
            payment["loan_id"]
        )
        relationship_errors += 1

if relationship_errors == 0:
    print("All payment loan relationships matched")

# Step 6: Validate payment calculations
calculation_errors = 0

for payment in payments:

    emi_amount = round(float(payment["emi_amount"]), 2)
    amount_paid = round(float(payment["amount_paid"]), 2)
    unpaid_amount = round(float(payment["unpaid_amount"]), 2)

    expected_unpaid = round(emi_amount - amount_paid, 2)

    if unpaid_amount != expected_unpaid:
        print(
            payment["payment_id"],
            "- Incorrect unpaid amount"
        )
        calculation_errors += 1

if calculation_errors == 0:
    print("All payment calculations matched")

# Step 7: Validate payment status
status_errors = 0

for payment in payments:

    emi_amount = round(float(payment["emi_amount"]), 2)
    amount_paid = round(float(payment["amount_paid"]), 2)

    if amount_paid == 0:
        expected_status = "MISSED"

    elif amount_paid < emi_amount:
        expected_status = "PARTIAL"

    elif amount_paid == emi_amount:
        expected_status = "PAID"

    else:
        expected_status = "INVALID"

    if payment["payment_status"] != expected_status:
        print(
            payment["payment_id"],
            "- Incorrect payment status"
        )
        status_errors += 1

if status_errors == 0:
    print("All payment statuses matched")

# Step 8: Load installment due dates
installment_due_dates = {}

with open("data/all_emi_schedules.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for installment in reader:

        key = (
            installment["loan_id"],
            installment["month"]
        )

        installment_due_dates[key] = date.fromisoformat(
            installment["due_date"]
        )

# Step 9: Validate payment dates
date_errors = 0

for payment in payments:

    key = (
        payment["loan_id"],
        payment["installment_number"]
    )

    if key not in installment_due_dates:
        print(
            payment["payment_id"],
            "- Installment not found"
        )
        date_errors += 1
        continue

    due_date = installment_due_dates[key]

    payment_date = date.fromisoformat(
        payment["payment_date"]
    )

    earliest_date = due_date
    latest_date = due_date + timedelta(days=10)

    if not earliest_date <= payment_date <= latest_date:
        print(
            payment["payment_id"],
            "- Invalid payment date:",
            payment["payment_date"]
        )
        date_errors += 1

if date_errors == 0:
    print("All payment dates matched")

# Step 10: Final validation summary
print("\n---------- VALIDATION SUMMARY ----------")

print("Total payment records:", len(payments))
print("Duplicate ID errors:", duplicate_errors)
print("Relationship errors:", relationship_errors)
print("Calculation errors:", calculation_errors)
print("Status errors:", status_errors)
print("Date errors:", date_errors)

# Step 11: Overall validation result
if (
    duplicate_errors == 0
    and relationship_errors == 0
    and calculation_errors == 0
    and status_errors == 0
    and date_errors == 0
):
    print("\nALL PAYMENT VALIDATIONS PASSED!")

else:
    print("\nSOME PAYMENT VALIDATIONS FAILED!")
