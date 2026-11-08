# Loan details
principal = 100000
annual_rate = 12
months = 12

# Convert annual interest into monthly decimal rate
monthly_rate = annual_rate / 12 / 100

# Calculate EMI
emi = (
    principal
    * monthly_rate
    * (1 + monthly_rate) ** months
) / (
    (1 + monthly_rate) ** months - 1
)

print("Loan Amount:", principal)
print("Annual Interest Rate:", annual_rate, "%")
print("Monthly Interest Rate:", monthly_rate)
print("Loan Duration:", months, "months")
print("Monthly EMI:", round(emi, 2))