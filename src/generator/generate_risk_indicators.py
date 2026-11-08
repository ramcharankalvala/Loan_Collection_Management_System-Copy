
import csv

# Step 1: Read delinquency records
with open("data/delinquency.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    delinquency_records = list(reader)

print("Total delinquency records:", len(delinquency_records))


# Step 2: Count missed installments for each loan
loan_missed_counts = {}

for record in delinquency_records:

    loan_id = record["loan_id"]
    status = record["installment_status"]

    if loan_id not in loan_missed_counts:
        loan_missed_counts[loan_id] = 0

    if status == "MISSED":
        loan_missed_counts[loan_id] += 1


# Step 3: Define deterministic synthetic test scenarios
risk_scenarios = {
    "LOAN-000001": {
        "hardship_flag": False,
        "dispute_flag": False,
        "contact_restricted": False
    },
    "LOAN-000002": {
        "hardship_flag": True,
        "dispute_flag": False,
        "contact_restricted": False
    },
    "LOAN-000003": {
        "hardship_flag": False,
        "dispute_flag": True,
        "contact_restricted": True
    },
    "LOAN-000004": {
        "hardship_flag": True,
        "dispute_flag": False,
        "contact_restricted": True
    },
    "LOAN-000005": {
        "hardship_flag": False,
        "dispute_flag": False,
        "contact_restricted": False
    }
}


# Step 4: Validate scenario coverage
for loan_id in loan_missed_counts:

    if loan_id not in risk_scenarios:
        raise ValueError(
            f"Missing risk scenario for loan: {loan_id}"
        )


# Step 5: Generate risk indicators
risk_records = []

for loan_id, missed_count in loan_missed_counts.items():

    # Calculate payment behaviour risk score
    if missed_count == 0:
        risk_score = 0

    elif missed_count == 1:
        risk_score = 10

    elif missed_count <= 3:
        risk_score = 20

    else:
        risk_score = 30

    # Identify repeated payment failures
    repeated_payment_failure = missed_count >= 3

    # Retrieve predefined synthetic scenario
    scenario = risk_scenarios[loan_id]

    hardship_flag = scenario["hardship_flag"]
    dispute_flag = scenario["dispute_flag"]
    contact_restricted = scenario["contact_restricted"]

    # Create risk record
    risk_record = {
        "loan_id": loan_id,
        "missed_installments": missed_count,
        "repeated_payment_failure": repeated_payment_failure,
        "hardship_flag": hardship_flag,
        "dispute_flag": dispute_flag,
        "contact_restricted": contact_restricted,
        "risk_score": risk_score,
        "data_source": "SYNTHETIC_TEST_DATA"
    }

    risk_records.append(risk_record)


# Step 6: Save risk indicators
with open("data/risk_indicators.csv", "w", newline="", encoding="utf-8") as file:

    fieldnames = [
        "loan_id",
        "missed_installments",
        "repeated_payment_failure",
        "hardship_flag",
        "dispute_flag",
        "contact_restricted",
        "risk_score",
        "data_source"
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(risk_records)


# Step 7: Display risk indicator results
print("\n========== RISK INDICATORS ==========")

for record in risk_records:

    print("\nLoan ID:", record["loan_id"])
    print("Missed installments:", record["missed_installments"])
    print("Repeated payment failure:", record["repeated_payment_failure"])
    print("Hardship:", record["hardship_flag"])
    print("Disputed debt:", record["dispute_flag"])
    print("Contact restricted:", record["contact_restricted"])
    print("Risk score:", record["risk_score"])


# Step 8: Final summary
print("\n========== RISK GENERATION SUMMARY ==========")
print("Total loans processed:", len(risk_records))
print("Total risk records generated:", len(risk_records))

if len(risk_records) == len(loan_missed_counts):
    print("ALL RISK INDICATORS GENERATED SUCCESSFULLY!")
else:
    print("RISK INDICATOR GENERATION FAILED!")
