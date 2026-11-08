
import csv

# Step 1: Load loan delinquency summary
with open("data/loan_delinquency_summary.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    loans = list(reader)


# Step 2: Load risk indicators
with open("data/risk_indicators.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    risk_records = list(reader)

print("Total loans loaded:", len(loans))
print("Total risk records loaded:", len(risk_records))


# Step 3: Build risk lookup and detect duplicates
risk_lookup = {}
duplicate_errors = 0

for risk in risk_records:

    loan_id = risk["loan_id"]

    if loan_id in risk_lookup:
        print("Duplicate risk record:", loan_id)
        duplicate_errors += 1
    else:
        risk_lookup[loan_id] = risk


# Step 4: Validate risk record relationships
missing_risk_errors = 0

for loan in loans:

    loan_id = loan["loan_id"]

    if loan_id not in risk_lookup:
        print("Missing risk record for:", loan_id)
        missing_risk_errors += 1

if duplicate_errors > 0 or missing_risk_errors > 0:
    raise ValueError("Risk record validation failed. Check the input CSV files.")


# Step 5: Calculate priority scores
priority_records = []

for loan in loans:

    loan_id = loan["loan_id"]

    outstanding = round(float(loan["total_outstanding"]), 2)
    dpd = int(loan["loan_dpd"])

    if outstanding < 0 or dpd < 0:
        raise ValueError(f"Invalid financial or DPD value for {loan_id}")

    # Balance score
    if outstanding == 0:
        balance_score = 0
    elif outstanding <= 10000:
        balance_score = 10
    elif outstanding <= 30000:
        balance_score = 20
    elif outstanding <= 50000:
        balance_score = 30
    else:
        balance_score = 40

    # DPD score
    if dpd == 0:
        dpd_score = 0
    elif dpd <= 30:
        dpd_score = 5
    elif dpd <= 60:
        dpd_score = 10
    elif dpd <= 90:
        dpd_score = 15
    elif dpd <= 180:
        dpd_score = 20
    elif dpd <= 360:
        dpd_score = 25
    else:
        dpd_score = 30

    # Retrieve risk information
    risk = risk_lookup[loan_id]

    risk_score = int(risk["risk_score"])

    if risk_score < 0:
        raise ValueError(f"Invalid risk score for {loan_id}")

    hardship_flag = risk["hardship_flag"] == "True"
    dispute_flag = risk["dispute_flag"] == "True"
    contact_restricted = risk["contact_restricted"] == "True"

    # Calculate total priority score
    priority_score = balance_score + dpd_score + risk_score

    # Step 6: Determine individual statuses

    if dispute_flag:
        dispute_status = "HOLD_FOR_DISPUTE_REVIEW"
    else:
        dispute_status = "NO_DISPUTE"

    if hardship_flag:
        hardship_status = "HARDSHIP_SUPPORT_REVIEW"
    else:
        hardship_status = "NO_HARDSHIP_FLAG"

    if contact_restricted:
        contact_status = "CONTACT_BLOCKED"
    else:
        contact_status = "CONTACT_ALLOWED"

    # Step 7: Determine main collection action
    # Priority: Dispute > Contact restriction > Hardship > Eligible

    if dispute_flag:
        action_status = "HOLD_FOR_DISPUTE_REVIEW"

    elif contact_restricted:
        action_status = "CONTACT_BLOCKED"

    elif hardship_flag:
        action_status = "HARDSHIP_SUPPORT_REVIEW"

    else:
        action_status = "ELIGIBLE_FOR_REVIEW"

    # Step 8: Store priority record
    priority_records.append({
        "loan_id": loan_id,
        "priority_score": priority_score,
        "outstanding": outstanding,
        "dpd": dpd,
        "risk_score": risk_score,
        "balance_score": balance_score,
        "dpd_score": dpd_score,
        "hardship_flag": hardship_flag,
        "dispute_flag": dispute_flag,
        "contact_restricted": contact_restricted,
        "dispute_status": dispute_status,
        "hardship_status": hardship_status,
        "contact_status": contact_status,
        "action_status": action_status
    })


# Step 9: Sort loans by priority
priority_records.sort(
    key=lambda record: (
        record["priority_score"],
        record["dpd"],
        record["outstanding"]
    ),
    reverse=True
)


# Step 10: Assign priority ranks
for index, record in enumerate(priority_records, start=1):
    record["priority_rank"] = index


# Step 11: Display collection priority
print("\n========== COLLECTION PRIORITY ==========")

for record in priority_records:

    print("\nPriority Rank:", record["priority_rank"])
    print("Loan ID:", record["loan_id"])
    print("Priority Score:", record["priority_score"])
    print("Outstanding:", round(record["outstanding"], 2))
    print("DPD:", record["dpd"])
    print("Risk Score:", record["risk_score"])
    print("Balance Score:", record["balance_score"])
    print("DPD Score:", record["dpd_score"])

    print("Hardship:", record["hardship_flag"])
    print("Dispute:", record["dispute_flag"])
    print("Contact Restricted:", record["contact_restricted"])

    print("Dispute Status:", record["dispute_status"])
    print("Hardship Status:", record["hardship_status"])
    print("Contact Status:", record["contact_status"])
    print("Action Status:", record["action_status"])


# Step 12: Save collection priority CSV
fieldnames = [
    "priority_rank",
    "loan_id",
    "priority_score",
    "outstanding",
    "dpd",
    "risk_score",
    "balance_score",
    "dpd_score",
    "hardship_flag",
    "dispute_flag",
    "contact_restricted",
    "dispute_status",
    "hardship_status",
    "contact_status",
    "action_status"
]

with open("data/collection_priority.csv", "w", newline="", encoding="utf-8") as file:

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(priority_records)


# Step 13: Final summary
print("\n========== PRIORITY GENERATION SUMMARY ==========")

print("Total loans prioritized:", len(priority_records))
print("Duplicate risk errors:", duplicate_errors)
print("Missing risk errors:", missing_risk_errors)

if len(priority_records) == len(loans) and duplicate_errors == 0 and missing_risk_errors == 0:
    print("ALL COLLECTION PRIORITIES GENERATED SUCCESSFULLY!")
else:
    print("COLLECTION PRIORITY GENERATION FAILED!")

print("Collection priority file saved successfully!")
