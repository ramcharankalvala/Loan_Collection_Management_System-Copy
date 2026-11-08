
import csv

# Step 1: Read delinquency records
with open("data/delinquency.csv", "r", newline="", encoding="utf-8") as file:

    reader = csv.DictReader(file)
    delinquency_records = list(reader)

print("Total delinquency records:", len(delinquency_records))


# Step 2: Create a dictionary for loan summaries
loan_summary = {}


# Step 3: Process every installment
for record in delinquency_records:

    loan_id = record["loan_id"]

    emi_amount = float(record["emi_amount"])
    amount_paid = float(record["amount_paid"])
    outstanding = float(record["outstanding_amount"])
    dpd = int(record["days_past_due"])

    status = record["installment_status"]

    # Create a summary for a loan if it does not exist
    if loan_id not in loan_summary:

        loan_summary[loan_id] = {
            "paid": 0,
            "partial": 0,
            "missed": 0,
            "total_emi": 0,
            "total_paid": 0,
            "outstanding": 0,
            "loan_dpd": 0
        }

    # Step 4: Count installment statuses
    if status == "PAID":
        loan_summary[loan_id]["paid"] += 1

    elif status == "PARTIAL":
        loan_summary[loan_id]["partial"] += 1

    elif status == "MISSED":
        loan_summary[loan_id]["missed"] += 1

    # Step 5: Calculate financial totals
    loan_summary[loan_id]["total_emi"] += emi_amount
    loan_summary[loan_id]["total_paid"] += amount_paid
    loan_summary[loan_id]["outstanding"] += outstanding

    # Step 6: Calculate loan-level DPD
    if outstanding > 0 and dpd > loan_summary[loan_id]["loan_dpd"]:
        loan_summary[loan_id]["loan_dpd"] = dpd


# Step 7: Save loan-level summary
with open("data/loan_delinquency_summary.csv", "w", newline="", encoding="utf-8") as file:

    fieldnames = [
        "loan_id",
        "paid_installments",
        "partial_installments",
        "missed_installments",
        "total_emi",
        "total_paid",
        "total_outstanding",
        "loan_dpd"
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()

    for loan_id, summary in loan_summary.items():

        output_record = {
            "loan_id": loan_id,
            "paid_installments": summary["paid"],
            "partial_installments": summary["partial"],
            "missed_installments": summary["missed"],
            "total_emi": round(summary["total_emi"], 2),
            "total_paid": round(summary["total_paid"], 2),
            "total_outstanding": round(summary["outstanding"], 2),
            "loan_dpd": summary["loan_dpd"]
        }

        writer.writerow(output_record)


# Step 8: Display summary
print("\n---------- LOAN DELINQUENCY SUMMARY ----------")

for loan_id, summary in loan_summary.items():

    print("\nLoan ID:", loan_id)
    print("Fully paid installments:", summary["paid"])
    print("Partially paid installments:", summary["partial"])
    print("Missed installments:", summary["missed"])
    print("Total outstanding:", round(summary["outstanding"], 2))
    print("Loan-level DPD:", summary["loan_dpd"])

print("\nTotal loans:", len(loan_summary))
print("Loan delinquency summary saved successfully!")
# Step 9: Validate total outstanding reconciliation

total_loan_outstanding = round(
    sum(summary["outstanding"] for summary in loan_summary.values()), 2
)

total_delinquency_outstanding = round(
    sum(float(record["outstanding_amount"]) for record in delinquency_records), 2
)

print("\n---------- RECONCILIATION CHECK ----------")
print("Delinquency outstanding:", total_delinquency_outstanding)
print("Loan summary outstanding:", total_loan_outstanding)

if total_loan_outstanding == total_delinquency_outstanding:
    print("Loan delinquency reconciliation PASSED!")
else:
    print("Loan delinquency reconciliation FAILED!")