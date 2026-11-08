
import csv
from datetime import date
from collections import defaultdict


# Step 1: Load promise records
with open("data/promises_to_pay.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    promises = list(reader)


# Step 2: Load loan records
with open("data/loans.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    loans = list(reader)


# Step 3: Load customer records
with open("data/customers.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    customers = list(reader)


# Step 4: Load payment records
with open("data/payments.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    payments = list(reader)


# Step 5: Load allocation records
with open("data/promise_payment_allocations.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    allocations = list(reader)


print("Total promises:", len(promises))
print("Total loans:", len(loans))
print("Total customers:", len(customers))
print("Total payments:", len(payments))
print("Total allocations:", len(allocations))


# Step 6: Check duplicate promise IDs
promise_ids = [
    promise["promise_id"] for promise in promises
]

duplicate_promise_errors = (
    len(promise_ids) - len(set(promise_ids))
)

if duplicate_promise_errors == 0:
    print("\nNo duplicate promise IDs")
else:
    print("\nDuplicate promise IDs found!")


# Step 7: Create lookup dictionaries
loan_lookup = {}
customer_ids = set()
promise_lookup = {}
payment_lookup = {}

for loan in loans:
    loan_lookup[loan["loan_id"]] = loan["customer_id"]

for customer in customers:
    customer_ids.add(customer["customer_id"])

for promise in promises:
    promise_lookup[promise["promise_id"]] = promise

for payment in payments:
    payment_lookup[payment["payment_id"]] = payment


# Step 8: Validate promise relationships
relationship_errors = 0

for promise in promises:

    promise_id = promise["promise_id"]
    loan_id = promise["loan_id"]
    customer_id = promise["customer_id"]

    if loan_id not in loan_lookup:
        print(promise_id, "- Invalid loan ID")
        relationship_errors += 1

    elif customer_id not in customer_ids:
        print(promise_id, "- Invalid customer ID")
        relationship_errors += 1

    elif loan_lookup[loan_id] != customer_id:
        print(promise_id, "- Customer does not belong to this loan")
        relationship_errors += 1

    else:
        print(promise_id, "- Loan and customer relationship matched")


# Step 9: Group allocations by promise and payment
allocations_by_promise = defaultdict(list)
allocated_by_payment = defaultdict(float)

allocation_ids = []
allocation_errors = 0

for allocation in allocations:

    allocation_id = allocation["allocation_id"]
    promise_id = allocation["promise_id"]
    payment_id = allocation["payment_id"]

    allocation_ids.append(allocation_id)

    if promise_id not in promise_lookup:
        print(allocation_id, "- Invalid promise ID")
        allocation_errors += 1
        continue

    if payment_id not in payment_lookup:
        print(allocation_id, "- Invalid payment ID")
        allocation_errors += 1
        continue

    promise = promise_lookup[promise_id]
    payment = payment_lookup[payment_id]

    allocated_amount = round(
        float(allocation["allocated_amount"]), 2
    )

    payment_date = date.fromisoformat(payment["payment_date"])
    allocation_date = date.fromisoformat(allocation["allocation_date"])

    created_date = date.fromisoformat(promise["created_date"])
    promise_date = date.fromisoformat(promise["promise_date"])

    if allocated_amount <= 0:
        print(allocation_id, "- Invalid allocated amount")
        allocation_errors += 1

    if promise["loan_id"] != payment["loan_id"]:
        print(allocation_id, "- Promise and payment loan mismatch")
        allocation_errors += 1

    if promise["customer_id"] != payment["customer_id"]:
        print(allocation_id, "- Promise and payment customer mismatch")
        allocation_errors += 1

    if not created_date <= payment_date <= promise_date:
        print(allocation_id, "- Payment outside promise period")
        allocation_errors += 1

    if allocation_date != payment_date:
        print(allocation_id, "- Allocation date does not match payment date")
        allocation_errors += 1

    allocations_by_promise[promise_id].append(allocation)

    allocated_by_payment[payment_id] += allocated_amount


# Step 10: Check duplicate allocation IDs
duplicate_allocation_errors = (
    len(allocation_ids) - len(set(allocation_ids))
)

if duplicate_allocation_errors == 0:
    print("\nNo duplicate allocation IDs")
else:
    print("\nDuplicate allocation IDs found!")


# Step 11: Check payment over-allocation
payment_overallocation_errors = 0

for payment_id, total_allocated in allocated_by_payment.items():

    actual_payment = round(
        float(payment_lookup[payment_id]["amount_paid"]), 2
    )

    if round(total_allocated, 2) > actual_payment:
        print(
            payment_id,
            "- Allocated more than actual payment"
        )
        payment_overallocation_errors += 1

if payment_overallocation_errors == 0:
    print("No payment has been over-allocated")


# Step 12: Calculate and validate promise balances
reference_date = date(2026, 11, 20)

fulfilled_count = 0
partial_count = 0
missed_count = 0
pending_count = 0

balance_errors = 0
promise_overallocation_errors = 0

print("\n---------- PROMISE VALIDATION ----------")

for promise in promises:

    promise_id = promise["promise_id"]

    promise_amount = round(
        float(promise["promise_amount"]), 2
    )

    promise_date = date.fromisoformat(
        promise["promise_date"]
    )

    # Calculate total payment allocated to this promise
    amount_paid = 0.0

    for allocation in allocations_by_promise[promise_id]:
        amount_paid += float(allocation["allocated_amount"])

    amount_paid = round(amount_paid, 2)

    # Check whether allocated amount exceeds promise amount
    if amount_paid > promise_amount:
        print(promise_id, "- Allocated more than promise amount")
        promise_overallocation_errors += 1

    # Calculate remaining promise amount
    remaining_amount = round(
        promise_amount - amount_paid, 2
    )

    # Derive expected promise status
    if amount_paid >= promise_amount:
        expected_status = "FULFILLED"

    elif amount_paid > 0:
        expected_status = "PARTIALLY_FULFILLED"

    elif reference_date > promise_date:
        expected_status = "MISSED"

    else:
        expected_status = "PENDING"

    # Compare calculated values with stored CSV values
    stored_paid = round(
        float(promise["amount_paid"]), 2
    )

    stored_remaining = round(
        float(promise["remaining_amount"]), 2
    )

    stored_status = promise["promise_status"]

    if stored_paid != amount_paid:
        print(promise_id, "- Paid amount mismatch")
        balance_errors += 1

    if stored_remaining != remaining_amount:
        print(promise_id, "- Remaining amount mismatch")
        balance_errors += 1

    if stored_status != expected_status:
        print(promise_id, "- Promise status mismatch")
        balance_errors += 1

    print("\nPromise ID:", promise_id)
    print("Promise amount:", promise_amount)
    print("Calculated paid amount:", amount_paid)
    print("Stored paid amount:", stored_paid)
    print("Calculated remaining amount:", remaining_amount)
    print("Stored remaining amount:", stored_remaining)
    print("Expected status:", expected_status)
    print("Stored status:", stored_status)

    # Count expected promise statuses
    if expected_status == "FULFILLED":
        fulfilled_count += 1

    elif expected_status == "PARTIALLY_FULFILLED":
        partial_count += 1

    elif expected_status == "MISSED":
        missed_count += 1

    elif expected_status == "PENDING":
        pending_count += 1


# Step 13: Final validation summary
print("\n---------- VALIDATION SUMMARY ----------")

print("Duplicate promise ID errors:", duplicate_promise_errors)
print("Relationship errors:", relationship_errors)
print("Allocation errors:", allocation_errors)
print("Duplicate allocation ID errors:", duplicate_allocation_errors)
print("Payment over-allocation errors:", payment_overallocation_errors)
print("Promise over-allocation errors:", promise_overallocation_errors)
print("Stored balance errors:", balance_errors)


# Step 14: Promise status summary
print("\n---------- PROMISE STATUS SUMMARY ----------")

print("Total promises:", len(promises))
print("Fulfilled promises:", fulfilled_count)
print("Partially fulfilled promises:", partial_count)
print("Missed promises:", missed_count)
print("Pending promises:", pending_count)


# Step 15: Overall validation result
if (
    duplicate_promise_errors == 0
    and relationship_errors == 0
    and allocation_errors == 0
    and duplicate_allocation_errors == 0
    and payment_overallocation_errors == 0
    and promise_overallocation_errors == 0
    and balance_errors == 0
):
    print("\nALL PROMISE VALIDATIONS PASSED!")

else:
    print("\nSOME PROMISE VALIDATIONS FAILED!")
