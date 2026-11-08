
import csv
from datetime import date

# Step 1: Set a fixed reference date
today = date(2026, 12, 31)

# Step 2: Create a list to store DPD records
dpd_records = []

# Step 3: Read EMI installment records
with open("data/all_emi_schedules.csv", "r", newline="", encoding="utf-8") as file:

    reader = csv.DictReader(file)

    for installment in reader:

        loan_id = installment["loan_id"]
        customer_id = installment["customer_id"]
        month = installment["month"]
        due_date = date.fromisoformat(installment["due_date"])

        # Step 4: Calculate DPD
        if today > due_date:
            dpd = (today - due_date).days
        else:
            dpd = 0

        # Step 5: Create DPD record
        record = {
            "loan_id": loan_id,
            "customer_id": customer_id,
            "installment_number": month,
            "due_date": due_date.isoformat(),
            "as_of_date": today.isoformat(),
            "days_past_due": dpd
        }

        dpd_records.append(record)

# Step 6: Save DPD records
with open("data/installment_dpd.csv", "w", newline="", encoding="utf-8") as file:

    fieldnames = [
        "loan_id",
        "customer_id",
        "installment_number",
        "due_date",
        "as_of_date",
        "days_past_due"
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(dpd_records)

# Step 7: Display results
print("Total installment records:", len(dpd_records))

print("\nFirst installment:")
print(dpd_records[0])

print("\nLast installment:")
print(dpd_records[-1])

print("\nDPD records saved successfully!")
