
import csv
from datetime import datetime

# Step 1: Load contact attempts

with open("data/contact_attempts.csv", "r", newline="", encoding="utf-8") as file:
    attempts = list(csv.DictReader(file))

print("Total contact attempts:", len(attempts))


# Step 2: Load collection cases

with open("data/collection_cases.csv", "r", newline="", encoding="utf-8") as file:
    cases = list(csv.DictReader(file))

print("Total collection cases:", len(cases))


# Step 3: Load contact preferences

with open("data/contact_preferences.csv", "r", newline="", encoding="utf-8") as file:
    preferences = list(csv.DictReader(file))

print("Total contact preferences:", len(preferences))

# Step 4: Check duplicate attempt IDs

attempt_ids = set()
duplicate_errors = 0

for attempt in attempts:

    attempt_id = attempt["attempt_id"]

    if attempt_id in attempt_ids:
        print("Duplicate attempt ID:", attempt_id)
        duplicate_errors += 1

    else:
        attempt_ids.add(attempt_id)

if duplicate_errors == 0:
    print("No duplicate contact attempt IDs")

print("Duplicate ID errors:", duplicate_errors)

# Step 5: Check collection case relationships

case_ids = set()

for case in cases:
    case_ids.add(case["case_id"])

relationship_errors = 0

for attempt in attempts:

    case_id = attempt["case_id"]

    if case_id not in case_ids:
        print("Invalid collection case relationship:", attempt["attempt_id"])
        relationship_errors += 1

    else:
        print(attempt["attempt_id"], "- Collection case matched")

print("Collection case relationship errors:", relationship_errors)

# Step 6: Create collection case lookup

case_lookup = {}

for case in cases:
    case_lookup[case["case_id"]] = case


# Step 7: Validate customer relationships

customer_errors = 0

for attempt in attempts:

    case_id = attempt["case_id"]

    case = case_lookup.get(case_id)

    if case is not None:

        if attempt["customer_id"] == case["customer_id"]:
            print(attempt["attempt_id"], "- Customer relationship matched")

        else:
            print(attempt["attempt_id"], "- Customer relationship error")
            customer_errors += 1

print("Customer relationship errors:", customer_errors)

# Step 8: Create customer preference lookup

preference_lookup = {}

for preference in preferences:
    preference_lookup[preference["customer_id"]] = preference


# Step 9: Validate allowed communication channels

channel_errors = 0

for attempt in attempts:

    customer_id = attempt["customer_id"]
    channel = attempt["channel"]

    preference = preference_lookup.get(customer_id)

    if preference is None:
        print(attempt["attempt_id"], "- Preference record missing")
        channel_errors += 1
        continue

    if channel == "PHONE":
        allowed = preference["phone_allowed"]

    elif channel == "SMS":
        allowed = preference["sms_allowed"]

    elif channel == "EMAIL":
        allowed = preference["email_allowed"]

    else:
        allowed = "False"

    if allowed == "True":
        print(attempt["attempt_id"], "-", channel, "allowed")

    else:
        print(attempt["attempt_id"], "-", channel, "NOT ALLOWED")
        channel_errors += 1

print("Channel permission errors:", channel_errors)

# Step 10: Validate customer opt-out status

opt_out_errors = 0

for attempt in attempts:

    customer_id = attempt["customer_id"]

    preference = preference_lookup.get(customer_id)

    if preference is None:
        opt_out_errors += 1
        print(attempt["attempt_id"], "- Preference record missing")

    elif preference["contact_opt_out"] == "True":
        opt_out_errors += 1
        print(attempt["attempt_id"], "- Customer opted out")

    else:
        print(attempt["attempt_id"], "- Customer has not opted out")

print("Opt-out validation errors:", opt_out_errors)

# Step 11: Validate contact time window

time_errors = 0

for attempt in attempts:

    customer_id = attempt["customer_id"]

    preference = preference_lookup.get(customer_id)

    if preference is None:
        time_errors += 1
        continue

    attempt_datetime = datetime.strptime(
        attempt["attempt_datetime"],
        "%Y-%m-%d %H:%M:%S"
    )

    attempt_time = attempt_datetime.strftime("%H:%M")

    start_time = preference["allowed_start_time"]
    end_time = preference["allowed_end_time"]

    if start_time <= attempt_time < end_time:
        print(attempt["attempt_id"], "- Contact time allowed")

    else:
        print(attempt["attempt_id"], "- Contact time NOT allowed")
        time_errors += 1

print("Contact time errors:", time_errors)

# Step 12: Validate channel outcomes

valid_outcomes = {
    "PHONE": ["ANSWERED", "NO_ANSWER", "BUSY", "FAILED"],
    "SMS": ["DELIVERED", "FAILED"],
    "EMAIL": ["DELIVERED", "BOUNCED"]
}

outcome_errors = 0

for attempt in attempts:

    channel = attempt["channel"]
    outcome = attempt["outcome"]

    if channel not in valid_outcomes:
        print(attempt["attempt_id"], "- Invalid channel")
        outcome_errors += 1

    elif outcome in valid_outcomes[channel]:
        print(attempt["attempt_id"], "- Outcome matched")

    else:
        print(attempt["attempt_id"], "- Invalid outcome")
        outcome_errors += 1

print("Outcome validation errors:", outcome_errors)

# Step 13: Validate case eligibility

eligibility_errors = 0

for attempt in attempts:

    case = case_lookup.get(attempt["case_id"])

    if case is None:
        eligibility_errors += 1
        print(attempt["attempt_id"], "- Collection case missing")
        continue

    if (
        case["case_status"] == "OPEN"
        and case["contact_status"] == "CONTACT_ALLOWED"
        and case["dispute_status"] == "NO_DISPUTE"
        and case["hardship_status"] == "NO_HARDSHIP_FLAG"
    ):
        print(attempt["attempt_id"], "- Case eligible for contact")

    else:
        print(attempt["attempt_id"], "- Case NOT eligible for contact")
        eligibility_errors += 1

print("Case eligibility errors:", eligibility_errors)
# Step 14: Final validation summary

total_errors = (
    duplicate_errors
    + relationship_errors
    + customer_errors
    + channel_errors
    + opt_out_errors
    + time_errors
    + outcome_errors
    + eligibility_errors
)

print("\n========== CONTACT VALIDATION SUMMARY ==========")

print("Total contact attempts:", len(attempts))
print("Total validation errors:", total_errors)

if total_errors == 0:
    print("ALL CONTACT ATTEMPT VALIDATIONS PASSED!")
else:
    print("CONTACT ATTEMPT VALIDATION FAILED!")