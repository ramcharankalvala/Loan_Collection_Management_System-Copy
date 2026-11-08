
import csv

# Step 1: Load collection cases
with open("data/collection_cases.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    cases = list(reader)

# Step 2: Load loans
with open("data/loans.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    loans = list(reader)

# Step 3: Load collection priority records
with open("data/collection_priority.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    priorities = list(reader)

print("Total collection cases:", len(cases))
print("Total loans:", len(loans))
print("Total priority records:", len(priorities))

# Step 4: Check duplicate collection case IDs

case_ids = []

for case in cases:
    case_ids.append(case["case_id"])

if len(case_ids) == len(set(case_ids)):
    print("No duplicate collection case IDs")
else:
    print("Duplicate collection case IDs found")

# Display duplicate count
duplicate_count = len(case_ids) - len(set(case_ids))

print("Duplicate case ID errors:", duplicate_count)

# Step 5: Validate loan relationships

loan_ids = set()

for loan in loans:
    loan_ids.add(loan["loan_id"])

relationship_errors = 0

for case in cases:

    if case["loan_id"] in loan_ids:
        print(case["case_id"], "- Loan relationship matched")
    else:
        print(case["case_id"], "- Invalid loan relationship")
        relationship_errors += 1

print("Loan relationship errors:", relationship_errors)

# Step 6: Validate customer relationships

loan_lookup = {}

for loan in loans:
    loan_lookup[loan["loan_id"]] = loan

customer_errors = 0

for case in cases:

    loan_id = case["loan_id"]

    if loan_id in loan_lookup:

        expected_customer_id = loan_lookup[loan_id]["customer_id"]

        if case["customer_id"] == expected_customer_id:
            print(case["case_id"], "- Customer relationship matched")
        else:
            print(case["case_id"], "- Customer relationship mismatch")
            customer_errors += 1

print("Customer relationship errors:", customer_errors)

# Step 7: Validate case status

case_status_errors = 0

for case in cases:

    if case["dispute_status"] == "HOLD_FOR_DISPUTE_REVIEW":
        expected_status = "ON_HOLD"
    else:
        expected_status = "OPEN"

    if case["case_status"] == expected_status:
        print(case["case_id"], "- Case status matched")
    else:
        print(case["case_id"], "- Case status mismatch")
        case_status_errors += 1

print("Case status errors:", case_status_errors)

# Step 8: Validate priority information

priority_lookup = {}

for priority in priorities:
    priority_lookup[priority["loan_id"]] = priority

priority_errors = 0

for case in cases:

    loan_id = case["loan_id"]

    if loan_id in priority_lookup:

        expected_priority = priority_lookup[loan_id]

        if (
            int(case["priority_rank"]) == int(expected_priority["priority_rank"])
            and int(case["priority_score"]) == int(expected_priority["priority_score"])
            and float(case["outstanding"]) == float(expected_priority["outstanding"])
            and int(case["dpd"]) == int(expected_priority["dpd"])
        ):
            print(case["case_id"], "- Priority information matched")
        else:
            print(case["case_id"], "- Priority information mismatch")
            priority_errors += 1

    else:
        print(case["case_id"], "- Priority record not found")
        priority_errors += 1

print("Priority information errors:", priority_errors)

# Step 9: Validate contact restriction

contact_errors = 0

for case in cases:

    loan_id = case["loan_id"]

    if loan_id in priority_lookup:

        priority = priority_lookup[loan_id]

        if priority["contact_restricted"] == "True":
            expected_contact_status = "CONTACT_BLOCKED"
        else:
            expected_contact_status = "CONTACT_ALLOWED"

        if case["contact_status"] == expected_contact_status:
            print(case["case_id"], "- Contact restriction matched")
        else:
            print(case["case_id"], "- Contact restriction mismatch")
            contact_errors += 1

    else:
        print(case["case_id"], "- Priority record not found")
        contact_errors += 1

print("Contact restriction errors:", contact_errors)

# Step 10: Validate hardship status

hardship_errors = 0

for case in cases:

    loan_id = case["loan_id"]

    if loan_id in priority_lookup:

        priority = priority_lookup[loan_id]

        if priority["hardship_flag"] == "True":
            expected_hardship_status = "HARDSHIP_SUPPORT_REVIEW"
        else:
            expected_hardship_status = "NO_HARDSHIP_FLAG"

        if case["hardship_status"] == expected_hardship_status:
            print(case["case_id"], "- Hardship status matched")
        else:
            print(case["case_id"], "- Hardship status mismatch")
            hardship_errors += 1

    else:
        print(case["case_id"], "- Priority record not found")
        hardship_errors += 1

print("Hardship status errors:", hardship_errors)

# Step 11: Validate dispute status

dispute_errors = 0

for case in cases:

    loan_id = case["loan_id"]

    if loan_id in priority_lookup:

        priority = priority_lookup[loan_id]

        if priority["dispute_flag"] == "True":
            expected_dispute_status = "HOLD_FOR_DISPUTE_REVIEW"
        else:
            expected_dispute_status = "NO_DISPUTE"

        if case["dispute_status"] == expected_dispute_status:
            print(case["case_id"], "- Dispute status matched")
        else:
            print(case["case_id"], "- Dispute status mismatch")
            dispute_errors += 1

    else:
        print(case["case_id"], "- Priority record not found")
        dispute_errors += 1

print("Dispute status errors:", dispute_errors)

# Step 12: Validate action status

action_errors = 0

for case in cases:

    loan_id = case["loan_id"]

    if loan_id in priority_lookup:

        priority = priority_lookup[loan_id]

        expected_action_status = priority["action_status"]

        if case["action_status"] == expected_action_status:
            print(case["case_id"], "- Action status matched")
        else:
            print(case["case_id"], "- Action status mismatch")
            action_errors += 1

    else:
        print(case["case_id"], "- Priority record not found")
        action_errors += 1

print("Action status errors:", action_errors)

# Step 13: Validate collection case count

count_errors = 0

if len(cases) == len(loans):
    print("Collection case count matched")
else:
    print("Collection case count mismatch")
    count_errors += 1

print("Collection case count errors:", count_errors)

# Step 14: Validate required fields

required_fields = [
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

missing_field_errors = 0

for case in cases:

    for field in required_fields:

        if case[field] == "":
            print(case["case_id"], "- Missing field:", field)
            missing_field_errors += 1

print("Missing required field errors:", missing_field_errors)

# Step 15: Validate numeric values

numeric_errors = 0

for case in cases:

    if float(case["outstanding"]) < 0:
        print(case["case_id"], "- Negative outstanding amount")
        numeric_errors += 1

    if int(case["dpd"]) < 0:
        print(case["case_id"], "- Negative DPD")
        numeric_errors += 1

    if int(case["priority_rank"]) <= 0:
        print(case["case_id"], "- Invalid priority rank")
        numeric_errors += 1

    if int(case["priority_score"]) < 0:
        print(case["case_id"], "- Negative priority score")
        numeric_errors += 1

print("Numeric validation errors:", numeric_errors)

# Step 16: Validate allowed status values

valid_case_statuses = ["OPEN", "ON_HOLD"]

valid_action_statuses = [
    "HOLD_FOR_DISPUTE_REVIEW",
    "CONTACT_BLOCKED",
    "HARDSHIP_SUPPORT_REVIEW",
    "ELIGIBLE_FOR_REVIEW"
]

valid_contact_statuses = ["CONTACT_BLOCKED", "CONTACT_ALLOWED"]

valid_hardship_statuses = [
    "HARDSHIP_SUPPORT_REVIEW",
    "NO_HARDSHIP_FLAG"
]

valid_dispute_statuses = [
    "HOLD_FOR_DISPUTE_REVIEW",
    "NO_DISPUTE"
]

status_errors = 0

for case in cases:

    if case["case_status"] not in valid_case_statuses:
        print(case["case_id"], "- Invalid case status")
        status_errors += 1

    if case["action_status"] not in valid_action_statuses:
        print(case["case_id"], "- Invalid action status")
        status_errors += 1

    if case["contact_status"] not in valid_contact_statuses:
        print(case["case_id"], "- Invalid contact status")
        status_errors += 1

    if case["hardship_status"] not in valid_hardship_statuses:
        print(case["case_id"], "- Invalid hardship status")
        status_errors += 1

    if case["dispute_status"] not in valid_dispute_statuses:
        print(case["case_id"], "- Invalid dispute status")
        status_errors += 1

print("Allowed status validation errors:", status_errors)

# Step 17: Final validation summary

total_errors = (
    duplicate_count
    + relationship_errors
    + customer_errors
    + case_status_errors
    + priority_errors
    + contact_errors
    + hardship_errors
    + dispute_errors
    + action_errors
    + count_errors
    + missing_field_errors
    + numeric_errors
    + status_errors
)

print("\n========== FINAL VALIDATION SUMMARY ==========")

print("Total collection cases:", len(cases))
print("Total validation errors:", total_errors)

if total_errors == 0:
    print("ALL COLLECTION CASE VALIDATIONS PASSED!")
else:
    print("COLLECTION CASE VALIDATION FAILED!")
