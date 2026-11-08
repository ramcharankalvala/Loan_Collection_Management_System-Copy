from faker import Faker

fake = Faker("en_IN")

customers = []

for i in range(1, 6):

    customer = {
        "customer_id": f"CUST-{i:06d}",
        "name": fake.name(),
        "email": fake.email(),
        "city": fake.city(),
        "phone": fake.phone_number()
    }

    customers.append(customer)

for customer in customers:
    print(customer)

print("Total customers:", len(customers))