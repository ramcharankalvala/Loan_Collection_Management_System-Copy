
import csv
from datetime import date

# Step 1: Create a list to store all EMI records
all_emi_records = []

# Step 2: Read loan records
with open("data/loans.csv", "r", newline="", encoding="utf-8") as file:

    reader = csv.DictReader(file)

    # Step 3: Process each loan
    for loan in reader:

        loan_id = loan["loan_id"]
        customer_id = loan["customer_id"]
        principal = int(loan["loan_amount"])

        annual_rate = 12
        months = 12

        monthly_rate = annual_rate / 12 / 100

        # Step 4: Calculate EMI
        emi = (
            principal * monthly_rate * (1 + monthly_rate) ** months
        ) / (
            (1 + monthly_rate) ** months - 1
        )

        emi = round(emi, 2)

        # Step 5: Generate monthly EMI schedule
        balance = principal

        for month in range(1, months + 1):

            # Generate due date for this installment
            due_date = date(2026, month, 5).isoformat()

            interest = round(balance * monthly_rate, 2)
            principal_paid = round(emi - interest, 2)

            # Adjust final installment
            if month == months:
                principal_paid = balance
                emi_for_month = round(interest + principal_paid, 2)
            else:
                emi_for_month = emi

            balance = round(balance - principal_paid, 2)

            # Create one monthly record
            record = {
                "loan_id": loan_id,
                "customer_id": customer_id,
                "month": month,
                "due_date": due_date,
                "emi": emi_for_month,
                "interest": interest,
                "principal_paid": principal_paid,
                "remaining_balance": balance
            }

            all_emi_records.append(record)

        print("Generated EMI schedule for:", loan_id)

# Step 6: Save all records into CSV
with open("data/all_emi_schedules.csv", "w", newline="", encoding="utf-8") as file:

    fieldnames = [
        "loan_id",
        "customer_id",
        "month",
        "due_date",
        "emi",
        "interest",
        "principal_paid",
        "remaining_balance"
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(all_emi_records)

print("--------------------------------")
print("Total EMI records:", len(all_emi_records))
print("All EMI schedules saved successfully!")
