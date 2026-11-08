
import csv
from datetime import datetime

# Step 1: Load customers
with open("data/customers.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    customers = list(reader)

# Step 2: Load contact preferences
with open("data/contact_preferences.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    preferences = list(reader)

print("Total customers:", len(customers))
print("Total preference records:", len(preferences))


# Step 3: Build customer ID lookup
customer_ids = set()

for customer in customers:
    customer_ids.add(customer["customer_id"])


# Step 4: Check duplicate preference IDs
preference_ids = set()
duplicate_errors = 0

for record in preferences:

    customer_id = record["customer_id"]

    if customer_id in preference_ids:
        print("Duplicate preference:", customer_id)
        duplicate_errors += 1
    else:
        preference_ids.add(customer_id)

print("Duplicate preference errors:", duplicate_errors)


# Step 5: Validate customer relationships
relationship_errors = 0

for record in preferences:

    customer_id = record["customer_id"]

    if customer_id in customer_ids:
        print(customer_id, "- Customer relationship matched")
    else:
        print(customer_id, "- Customer relationship ERROR")
        relationship_errors += 1

print("Customer relationship errors:", relationship_errors)


# Step 6: Validate boolean values
boolean_errors = 0

boolean_fields = [
    "phone_allowed",
    "sms_allowed",
    "email_allowed",
    "contact_opt_out"
]

for record in preferences:

    for field in boolean_fields:

        if record[field] not in ["True", "False"]:
            print(record["customer_id"], "-", field, "ERROR")
            boolean_errors += 1

print("Boolean validation errors:", boolean_errors)


# Step 7: Validate permitted contact hours
time_errors = 0

for record in preferences:

    try:
        start_time = datetime.strptime(
            record["allowed_start_time"], "%H:%M"
        ).time()

        end_time = datetime.strptime(
            record["allowed_end_time"], "%H:%M"
        ).time()

        if start_time >= end_time:
            print(record["customer_id"], "- Invalid contact hours")
            time_errors += 1

    except ValueError:
        print(record["customer_id"], "- Invalid time format")
        time_errors += 1

print("Contact time errors:", time_errors)


# Step 8: Validate preference count
count_errors = 0

if len(preferences) == len(customers):
    print("Customer and preference counts matched")
else:
    print("Customer and preference counts ERROR")
    count_errors += 1

# Step 9: Final validation summary
total_errors = (
    duplicate_errors
    + relationship_errors
    + boolean_errors
    + time_errors
    + count_errors
)

print("\n========== FINAL VALIDATION SUMMARY ==========")
print("Total preference records:", len(preferences))
print("Total validation errors:", total_errors)

if total_errors == 0:
    print("ALL CONTACT PREFERENCE VALIDATIONS PASSED!")
else:
    print("CONTACT PREFERENCE VALIDATION FAILED!")
