
import csv
from src.database.db_connection import get_connection

connection = None
cursor = None

try:
    # Step 1: Connect to MySQL
    connection = get_connection()
    cursor = connection.cursor()

    # Step 2: Read Promise to Pay records
    records = []

    with open(
        "data/promises_to_pay.csv",
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            records.append((
                row["promise_id"],
                row["loan_id"],
                row["customer_id"],
                float(row["promise_amount"]),
                row["promise_date"],
                row["created_date"],
                float(row["amount_paid"]),
                float(row["remaining_amount"]),
                row["promise_status"]
            ))

    print("Total Promise to Pay records loaded:", len(records))

    # Step 3: Insert or update records
    query = """
    INSERT INTO promises_to_pay (
        promise_id,
        loan_id,
        customer_id,
        promise_amount,
        promise_date,
        created_date,
        amount_paid,
        remaining_amount,
        promise_status
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)

    ON DUPLICATE KEY UPDATE
        loan_id = VALUES(loan_id),
        customer_id = VALUES(customer_id),
        promise_amount = VALUES(promise_amount),
        promise_date = VALUES(promise_date),
        created_date = VALUES(created_date),
        amount_paid = VALUES(amount_paid),
        remaining_amount = VALUES(remaining_amount),
        promise_status = VALUES(promise_status)
    """

    cursor.executemany(query, records)

    # Step 4: Commit changes
    connection.commit()

    print("Promise to Pay records processed:", cursor.rowcount)
    print("Promise to Pay records imported successfully!")

except Exception as error:

    if connection is not None and connection.is_connected():
        connection.rollback()

    print("Promise to Pay import failed:", error)

finally:

    if cursor is not None:
        cursor.close()

    if connection is not None and connection.is_connected():
        connection.close()
        print("Database connection closed.")
