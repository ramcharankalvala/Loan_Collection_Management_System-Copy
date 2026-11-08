
import csv

# Step 1: Load collection cases

with open("data/collection_cases.csv", "r", newline="", encoding="utf-8") as file:
    cases = list(csv.DictReader(file))

print("Total collection cases:", len(cases))


# Step 2: Load contact preferences

with open("data/contact_preferences.csv", "r", newline="", encoding="utf-8") as file:
    preferences = list(csv.DictReader(file))

print("Total contact preferences:", len(preferences))


# Step 3: Create preference lookup

preference_lookup = {}

for preference in preferences:
    preference_lookup[preference["customer_id"]] = preference


# Step 4: Define simulated attempt details

attempt_plan = [
    ("PHONE", "10:00:00", "NO_ANSWER", "phone_allowed"),
    ("SMS", "11:00:00", "DELIVERED", "sms_allowed"),
    ("EMAIL", "14:00:00", "DELIVERED", "email_allowed")
]


# Step 5: Check eligibility and generate attempts

contact_attempts = []
eligible_cases = []

for case in cases:

    preference = preference_lookup.get(case["customer_id"])

    if preference is None:
        continue

    if (
        case["case_status"] == "OPEN"
        and case["contact_status"] == "CONTACT_ALLOWED"
        and case["dispute_status"] == "NO_DISPUTE"
        and case["hardship_status"] == "NO_HARDSHIP_FLAG"
        and preference["contact_opt_out"] == "False"
    ):

        eligible_cases.append(case)

        attempt_number = 1

        for channel, time, outcome, preference_field in attempt_plan:

            if preference[preference_field] == "True":

                start_time = preference["allowed_start_time"]
                end_time = preference["allowed_end_time"]

                if start_time <= time < end_time:

                    attempt = {
                        "attempt_id": f"CTP-{case['case_id']}-{attempt_number:03d}",
                        "case_id": case["case_id"],
                        "loan_id": case["loan_id"],
                        "customer_id": case["customer_id"],
                        "attempt_datetime": f"2026-11-20 {time}",
                        "channel": channel,
                        "outcome": outcome,
                        "data_source": "SYNTHETIC_TEST_DATA"
                    }

                    contact_attempts.append(attempt)
                    attempt_number += 1


# Step 6: Save contact attempts

fieldnames = [
    "attempt_id",
    "case_id",
    "loan_id",
    "customer_id",
    "attempt_datetime",
    "channel",
    "outcome",
    "data_source"
]

with open("data/contact_attempts.csv", "w", newline="", encoding="utf-8") as file:

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(contact_attempts)


# Step 7: Display results

print("\n---------- CONTACT ATTEMPTS ----------")

for attempt in contact_attempts:

    print(attempt["attempt_id"], "-", attempt["channel"], "-", attempt["outcome"])

print("\nEligible cases:", len(eligible_cases))
print("Total contact attempts generated:", len(contact_attempts))
print("Contact attempts saved successfully!")
