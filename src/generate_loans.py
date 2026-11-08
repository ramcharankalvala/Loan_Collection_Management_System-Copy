import csv
import random

random.seed(20261022)
# Step 1: Load customers
customers = []

with open("data/customers.csv", "r", newline="", encoding="utf-8") as file:

    reader = csv.DictReader(file)

    for row in reader:
        customers.append(row)

print("Total customers loaded:", len(customers))


# Step 2: Generate loans
loans = []

for i in range(1, 6):

    loan = {
        "loan_id": f"LOAN-{i:06d}",
        "customer_id": customers[i - 1]["customer_id"],
"loan_amount": random.choice([50000, 100000, 150000, 200000])    }

    loans.append(loan)


# Step 3: Display loans
for loan in loans:
    print(loan)

print("Total loans generated:", len(loans))
# Save loans into CSV
with open("data/loans.csv", "w", newline="", encoding="utf-8") as file:

    fieldnames = ["loan_id", "customer_id", "loan_amount"]

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()

    writer.writerows(loans)

print("Loan data saved successfully!")
# Validate customer IDs
customer_ids = []

for customer in customers:
    customer_ids.append(customer["customer_id"])

for loan in loans:
    if loan["customer_id"] in customer_ids:
        print(loan["loan_id"], "- Valid customer ID")
    else:
        print(loan["loan_id"], "- Invalid customer ID")