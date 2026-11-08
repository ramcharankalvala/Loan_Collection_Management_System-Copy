
import csv

# Step 1: Load original loan amounts
loan_amounts = {}

with open("data/loans.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for loan in reader:
        loan_id = loan["loan_id"]
        loan_amount = float(loan["loan_amount"])

        loan_amounts[loan_id] = loan_amount


# Step 2: Store EMI records for each loan
loan_records = {}

# Step 3: Read EMI schedule
with open("data/all_emi_schedules.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for record in reader:
        loan_id = record["loan_id"]

        if loan_id not in loan_records:
            loan_records[loan_id] = []

        loan_records[loan_id].append(record)


# Step 4: Validate relationship between loans and EMI schedules
relationship_errors = 0

for loan_id in loan_records:
    if loan_id not in loan_amounts:
        print(loan_id, "- EMI schedule has no matching loan record")
        relationship_errors += 1

for loan_id in loan_amounts:
    if loan_id not in loan_records:
        print(loan_id, "- Loan has no EMI schedule")
        relationship_errors += 1

if relationship_errors == 0:
    print("Loan and EMI schedule relationships matched")


# Step 5: Validate each loan
for loan_id, records in loan_records.items():

    # Sort records by installment month
    records.sort(key=lambda record: int(record["month"]))

    # Check installment count
    if len(records) == 12:
        print(loan_id, "- Installment count matched")
    else:
        print(loan_id, "- Incorrect installment count")

    # Check duplicate months
    months = [int(record["month"]) for record in records]

    if len(months) != len(set(months)):
        print(loan_id, "- Duplicate months found")
    else:
        print(loan_id, "- No duplicate months")

    # Check missing months
    expected_months = set(range(1, 13))
    actual_months = set(months)

    missing_months = expected_months - actual_months

    if missing_months:
        print(loan_id, "- Missing months:", sorted(missing_months))
    else:
        print(loan_id, "- No missing months")

    # Check EMI calculation
    for record in records:

        emi = round(float(record["emi"]), 2)
        interest = round(float(record["interest"]), 2)
        principal_paid = round(float(record["principal_paid"]), 2)

        expected_emi = round(interest + principal_paid, 2)

        if emi != expected_emi:
            print(loan_id, "- Incorrect EMI in month:", record["month"])
            break

    else:
        print(loan_id, "- All EMI calculations matched")

    # Check monthly balance calculation
    if loan_id in loan_amounts:

        previous_balance = loan_amounts[loan_id]
        balance_errors = 0

        for record in records:

            principal_paid = round(float(record["principal_paid"]), 2)
            remaining_balance = round(float(record["remaining_balance"]), 2)

            expected_balance = round(
                previous_balance - principal_paid, 2
            )

            if remaining_balance != expected_balance:
                print(
                    loan_id,
                    "- Incorrect balance in month:",
                    record["month"]
                )
                balance_errors += 1

            previous_balance = remaining_balance

        if balance_errors == 0:
            print(loan_id, "- Monthly balance calculations matched")

    # Check final balance
    if records:
        final_balance = round(
            float(records[-1]["remaining_balance"]), 2
        )

        if final_balance == 0:
            print(loan_id, "- Final balance matched")
        else:
            print(loan_id, "- Incorrect final balance:", final_balance)
    else:
        print(loan_id, "- No EMI records found")

    print("-------------------------")


# Step 6: Total loans validated
print("Total loans validated:", len(loan_records))
print("\n========== EMI VALIDATION SUMMARY ==========")

if relationship_errors == 0:
    print("Loan relationships: PASSED")
else:
    print("Loan relationships: FAILED")

print("Total loans validated:", len(loan_records))
print("Expected EMI records:", len(loan_amounts) * 12)
print("Actual EMI records:", sum(len(records) for records in loan_records.values()))