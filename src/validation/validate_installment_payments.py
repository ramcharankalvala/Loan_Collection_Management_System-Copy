
import csv

# Step 1: Load EMI installments
with open("data/all_emi_schedules.csv", "r", newline="", encoding="utf-8") as file:
    installments = list(csv.DictReader(file))

print("Total installments:", len(installments))


# Step 2: Load actual payments
with open("data/payments.csv", "r", newline="", encoding="utf-8") as file:
    payments = list(csv.DictReader(file))

print("Total actual payments:", len(payments))


# Step 3: Build installment lookup
installment_lookup = {}

for installment in installments:
    key = (installment["loan_id"], installment["month"])
    installment_lookup[key] = installment


# Step 4: Build payment lookup and detect duplicates
payment_lookup = {}
duplicate_errors = 0

for payment in payments:
    key = (payment["loan_id"], payment["installment_number"])

    if key in payment_lookup:
        print("Duplicate payment found:", key)
        duplicate_errors += 1
    else:
        payment_lookup[key] = payment

print("Payment lookup entries:", len(payment_lookup))


# Step 5: Validate payment relationships and amounts
relationship_errors = 0
amount_errors = 0

for key, payment in payment_lookup.items():

    if key not in installment_lookup:
        print("Payment has no matching EMI installment:", key)
        relationship_errors += 1
        continue

    amount_paid = round(float(payment["amount_paid"]), 2)
    emi_amount = round(float(installment_lookup[key]["emi"]), 2)

    if amount_paid < 0:
        print("Negative payment amount:", key)
        amount_errors += 1

    elif amount_paid > emi_amount:
        print("Payment exceeds EMI amount:", key)
        amount_errors += 1


# Step 6: Match installments with payments
matched_count = 0
unmatched_count = 0

for key in installment_lookup:

    if key in payment_lookup:
        matched_count += 1
    else:
        unmatched_count += 1

print("Installments with payment records:", matched_count)
print("Installments without payment records:", unmatched_count)


# Step 7: Calculate payment statuses and totals
paid_count = 0
partial_count = 0
missed_count = 0

total_emi_amount = 0
total_amount_paid = 0
total_outstanding = 0

loan_summary = {}

for key, installment in installment_lookup.items():

    loan_id = installment["loan_id"]
    emi_amount = round(float(installment["emi"]), 2)

    amount_paid = 0

    if key in payment_lookup:
        amount_paid = round(
            float(payment_lookup[key]["amount_paid"]), 2
        )

    outstanding = round(emi_amount - amount_paid, 2)

    total_emi_amount += emi_amount
    total_amount_paid += amount_paid
    total_outstanding += outstanding

    if amount_paid <= 0:
        missed_count += 1
        status = "MISSED"

    elif amount_paid < emi_amount:
        partial_count += 1
        status = "PARTIAL"

    else:
        paid_count += 1
        status = "PAID"

    if loan_id not in loan_summary:
        loan_summary[loan_id] = {
            "paid": 0,
            "partial": 0,
            "missed": 0,
            "outstanding": 0
        }

    loan_summary[loan_id][status.lower() if status != "PAID" else "paid"] += 1
    loan_summary[loan_id]["outstanding"] += outstanding


# Step 8: Display overall payment summary
print("\n========== PAYMENT SUMMARY ==========")

print("Fully paid installments:", paid_count)
print("Partially paid installments:", partial_count)
print("Missed installments:", missed_count)

print("Total classified:", paid_count + partial_count + missed_count)

print("Total EMI amount:", round(total_emi_amount, 2))
print("Total amount paid:", round(total_amount_paid, 2))
print("Total outstanding:", round(total_outstanding, 2))


# Step 9: Validate payment reconciliation
reconciliation_errors = 0

calculated_total = round(
    total_amount_paid + total_outstanding, 2
)

if calculated_total == round(total_emi_amount, 2):
    print("Payment reconciliation matched")
else:
    print("Payment reconciliation FAILED")
    reconciliation_errors += 1


# Step 10: Display loan-wise summary
print("\n========== LOAN-WISE PAYMENT SUMMARY ==========")

for loan_id, summary in loan_summary.items():

    print("\nLoan ID:", loan_id)
    print("Fully paid:", summary["paid"])
    print("Partially paid:", summary["partial"])
    print("Missed:", summary["missed"])
    print("Outstanding:", round(summary["outstanding"], 2))


# Step 11: Final validation summary
total_errors = (
    duplicate_errors
    + relationship_errors
    + amount_errors
    + reconciliation_errors
)

print("\n========== FINAL VALIDATION SUMMARY ==========")
print("Total EMI installments:", len(installments))
print("Total payment records:", len(payments))
print("Duplicate errors:", duplicate_errors)
print("Relationship errors:", relationship_errors)
print("Payment amount errors:", amount_errors)
print("Reconciliation errors:", reconciliation_errors)
print("Total validation errors:", total_errors)

if total_errors == 0:
    print("ALL INSTALLMENT PAYMENT VALIDATIONS PASSED!")
else:
    print("INSTALLMENT PAYMENT VALIDATION FAILED!")
