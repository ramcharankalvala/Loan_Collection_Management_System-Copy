from faker import Faker
import csv

fake = Faker("en_IN")
fake.seed_instance(20261022)
customers = []

# Generate 5 customers
for i in range(1, 1001):

    customer = {
        "customer_id": f"CUST-{i:06d}",
        "name": fake.name(),
        "email": fake.email(),
        "city": fake.city(),
        "phone": fake.phone_number()
    }

    customers.append(customer)

# Save customers into CSV
with open("data/customers.csv", "w", newline="", encoding="utf-8") as file:

    fieldnames = ["customer_id", "name", "email", "city", "phone"]

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()

    writer.writerows(customers)

print("Customer data saved successfully!")
print("Total customers:", len(customers))