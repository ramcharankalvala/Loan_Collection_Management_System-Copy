
import csv

# Step 1: Read customer records
with open("data/customers.csv", "r", newline="", encoding="utf-8") as file:

    reader = csv.DictReader(file)
    customers = list(reader)

print("Total customers loaded:", len(customers))


# Step 2: Define contact preference scenarios
preference_scenarios = {
    "CUST-000001": {
        "phone_allowed": True,
        "sms_allowed": True,
        "email_allowed": True,
        "contact_opt_out": False
    },
    "CUST-000002": {
        "phone_allowed": True,
        "sms_allowed": True,
        "email_allowed": True,
        "contact_opt_out": False
    },
    "CUST-000003": {
        "phone_allowed": True,
        "sms_allowed": True,
        "email_allowed": True,
        "contact_opt_out": False
    },
    "CUST-000004": {
        "phone_allowed": True,
        "sms_allowed": False,
        "email_allowed": True,
        "contact_opt_out": False
    },
    "CUST-000005": {
        "phone_allowed": True,
        "sms_allowed": True,
        "email_allowed": True,
        "contact_opt_out": False
    }
}


# Step 3: Generate preferences
preference_records = []

for customer in customers:

    customer_id = customer["customer_id"]

    # Use predefined scenarios for the first five customers
    if customer_id in preference_scenarios:
        scenario = preference_scenarios[customer_id]

    else:
        # Synthetic defaults for other customers
        scenario = {
            "phone_allowed": True,
            "sms_allowed": True,
            "email_allowed": True,
            "contact_opt_out": False
        }

    preference_record = {
        "customer_id": customer_id,
        "phone_allowed": scenario["phone_allowed"],
        "sms_allowed": scenario["sms_allowed"],
        "email_allowed": scenario["email_allowed"],
        "contact_opt_out": scenario["contact_opt_out"],
        "allowed_start_time": "09:00",
        "allowed_end_time": "18:00",
        "data_source": "SYNTHETIC_TEST_DATA"
    }

    preference_records.append(preference_record)


# Step 4: Save contact preferences
with open("data/contact_preferences.csv", "w", newline="", encoding="utf-8") as file:

    fieldnames = [
        "customer_id",
        "phone_allowed",
        "sms_allowed",
        "email_allowed",
        "contact_opt_out",
        "allowed_start_time",
        "allowed_end_time",
        "data_source"
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(preference_records)


# Step 5: Display summary
print("\n---------- CONTACT PREFERENCES ----------")

for record in preference_records[:5]:

    print("\nCustomer ID:", record["customer_id"])
    print("Phone allowed:", record["phone_allowed"])
    print("SMS allowed:", record["sms_allowed"])
    print("Email allowed:", record["email_allowed"])
    print("Contact opt-out:", record["contact_opt_out"])
    print("Permitted hours:",
          record["allowed_start_time"],
          "to",
          record["allowed_end_time"])

print("\nTotal preference records:", len(preference_records))
print("Contact preferences saved successfully!")
