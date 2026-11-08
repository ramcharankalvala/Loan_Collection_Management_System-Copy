
import csv

# Step 1: Load loans from CSV
loans = []

with open("data/loans.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        loans.append(row)

print("Total loans loaded:", len(loans))


# Step 2: Generate installments
installments = []

for loan in loans:

    loan_id = loan["loan_id"]
    loan_amount = int(loan["loan_amount"])

    # Divide loan amount into 3 installments
    base_amount = loan_amount // 3
    remainder = loan_amount % 3

    for i in range(1, 4):

        installment_amount = base_amount

        # Add remaining amount to the third installment
        if i == 3:
            installment_amount += remainder

        installment = {
            "installment_id": f"INS-{loan_id}-{i:03d}",
            "loan_id": loan_id,
            "installment_number": i,
            "installment_amount": installment_amount
        }

        installments.append(installment)


# Step 3: Display installments
for installment in installments:
    print(installment)

print("Total installments generated:", len(installments))


# Step 4: Save installments into CSV
with open("data/installments.csv", "w", newline="", encoding="utf-8") as file:

    fieldnames = [
        "installment_id",
        "loan_id",
        "installment_number",
        "installment_amount"
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(installments)

print("Installment data saved successfully!")


# Step 5: Validate installment amounts
print("\n--- INSTALLMENT VALIDATION ---")

for loan in loans:

    loan_id = loan["loan_id"]
    loan_amount = int(loan["loan_amount"])

    total_installments = 0

    for installment in installments:

        if installment["loan_id"] == loan_id:
            total_installments += installment["installment_amount"]

    if total_installments == loan_amount:
        print(loan_id, "- Amount matched")
    else:
        print(loan_id, "- Amount mismatch")


# Step 6: Calculate monthly interest rate
print("\n--- INTEREST RATE CALCULATION ---")

annual_rate = 18

monthly_rate = annual_rate / 12 / 100

print("Annual interest rate:", annual_rate, "%")
print("Monthly interest rate:", monthly_rate)
