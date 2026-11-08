
import csv

# Step 1: Loan details
principal = 100000
annual_rate = 12
months = 12

# Convert annual interest rate into monthly interest rate
monthly_rate = annual_rate / 12 / 100

# Step 2: Calculate monthly EMI
emi = (
    principal * monthly_rate * (1 + monthly_rate) ** months
) / (
    (1 + monthly_rate) ** months - 1
)

emi = round(emi, 2)

print("Monthly EMI:", emi)

# Step 3: Check first month's interest
interest = principal * monthly_rate
print("First month interest:", round(interest, 2))

# Step 4: Calculate first month's principal payment
principal_paid = emi - interest
print("First month principal paid:", round(principal_paid, 2))

# Step 5: Calculate remaining balance after first month
remaining_balance = principal - principal_paid
print("Remaining balance after first month:", round(remaining_balance, 2))

# Step 6: Prepare a list to store all monthly records
emi_records = []

# Step 7: Generate the complete EMI schedule
balance = principal

for month in range(1, months + 1):

    # Calculate monthly interest
    interest = round(balance * monthly_rate, 2)

    # Calculate principal portion
    principal_paid = round(emi - interest, 2)

    # Adjust the final payment to clear the remaining balance
    if month == months:
        principal_paid = balance
        emi_for_month = round(interest + principal_paid, 2)
    else:
        emi_for_month = emi

    # Update remaining loan balance
    balance = round(balance - principal_paid, 2)

    # Store monthly EMI details
    record = {
        "month": month,
        "emi": emi_for_month,
        "interest": interest,
        "principal_paid": principal_paid,
        "remaining_balance": balance
    }

    emi_records.append(record)

    print(
        "Month:", month,
        "| EMI:", emi_for_month,
        "| Interest:", interest,
        "| Principal:", principal_paid,
        "| Balance:", balance
    )

# Step 8: Check whether the loan is fully repaid
if balance == 0:
    print("Loan fully repaid!")
else:
    print("Loan balance remaining:", balance)

# Step 9: Save EMI records into a CSV file
with open("data/emi_schedule.csv", "w", newline="", encoding="utf-8") as file:

    fieldnames = [
        "month",
        "emi",
        "interest",
        "principal_paid",
        "remaining_balance"
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(emi_records)

print("EMI schedule saved successfully!")
print("Total EMI records:", len(emi_records))
