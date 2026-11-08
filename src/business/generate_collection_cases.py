
import csv


# Step 1: Load loan records
with open("data/loans.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    loans = list(reader)


# Step 2: Load collection priority records
with open("data/collection_priority.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    priority_records = list(reader)


print("Total loans loaded:", len(loans))
print("Total priority records loaded:", len(priority_records))


# Step 3: Create loan lookup and check duplicates
loan_lookup = {}
duplicate_loan_errors = 0

for loan in loans:
    loan_id = loan["loan_id"]

    if loan_id in loan_lookup:
        print("ERROR: Duplicate loan ID:", loan_id)
        duplicate_loan_errors += 1
    else:
        loan_lookup[loan_id] = loan

print("Total loans in lookup:", len(loan_lookup))


# Step 4: Validate priority records
priority_loan_ids = set()
missing_loan_errors = 0
duplicate_priority_errors = 0

for priority in priority_records:
    loan_id = priority["loan_id"]

    if loan_id in priority_loan_ids:
        print("ERROR: Duplicate priority record:", loan_id)
        duplicate_priority_errors += 1

    priority_loan_ids.add(loan_id)

    if loan_id not in loan_lookup:
        print("ERROR: Loan not found:", loan_id)
        missing_loan_errors += 1


# Stop if relationship errors exist
if (
    duplicate_loan_errors > 0
    or duplicate_priority_errors > 0
    or missing_loan_errors > 0
):
    raise ValueError("Collection case generation stopped due to validation errors.")


# Step 5: Create collection case records
collection_cases = []

for priority in priority_records:

    loan_id = priority["loan_id"]
    loan = loan_lookup[loan_id]

    # Generate collection case ID
    case_id = f"COL-2026-{len(collection_cases) + 1:06d}"

    # Determine case status
    if priority["dispute_flag"].strip().lower() == "true":
        case_status = "ON_HOLD"
    else:
        case_status = "OPEN"

    case = {
        "case_id": case_id,
        "loan_id": loan_id,
        "customer_id": loan["customer_id"],
        "priority_rank": int(priority["priority_rank"]),
        "priority_score": int(priority["priority_score"]),
        "outstanding": float(priority["outstanding"]),
        "dpd": int(priority["dpd"]),
        "case_status": case_status,
        "action_status": priority["action_status"],
        "dispute_status": priority["dispute_status"],
        "hardship_status": priority["hardship_status"],
        "contact_status": priority["contact_status"]
    }

    collection_cases.append(case)


# Step 6: Display collection case information
print("\n========== COLLECTION CASES ==========")

for case in collection_cases:

    print("\nCase ID:", case["case_id"])
    print("Loan ID:", case["loan_id"])
    print("Customer ID:", case["customer_id"])
    print("Priority Rank:", case["priority_rank"])
    print("Priority Score:", case["priority_score"])
    print("Outstanding:", round(case["outstanding"], 2))
    print("DPD:", case["dpd"])
    print("Case Status:", case["case_status"])
    print("Action Status:", case["action_status"])
    print("Dispute Status:", case["dispute_status"])
    print("Hardship Status:", case["hardship_status"])
    print("Contact Status:", case["contact_status"])


# Step 7: Save collection cases to CSV
fieldnames = [
    "case_id",
    "loan_id",
    "customer_id",
    "priority_rank",
    "priority_score",
    "outstanding",
    "dpd",
    "case_status",
    "action_status",
    "dispute_status",
    "hardship_status",
    "contact_status"
]

with open("data/collection_cases.csv", "w", newline="", encoding="utf-8") as file:

    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(collection_cases)


# Step 8: Final summary
print("\n========== COLLECTION CASE SUMMARY ==========")
print("Total collection cases created:", len(collection_cases))
print("Duplicate loan errors:", duplicate_loan_errors)
print("Duplicate priority errors:", duplicate_priority_errors)
print("Missing loan errors:", missing_loan_errors)

if len(collection_cases) == len(priority_records):
    print("ALL COLLECTION CASES GENERATED SUCCESSFULLY!")
else:
    print("COLLECTION CASE GENERATION FAILED!")

print("Collection cases saved successfully!")
