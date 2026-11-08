
import csv
from src.database.db_connection import get_connection

connection = None
cursor = None

try:
    # Step 1: Connect to MySQL
    connection = get_connection()
    cursor = connection.cursor()

    # Step 2: Read payment allocation records
    records = []

    with open(
        "data/promise_payment_allocations.csv",
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            records.append((
                row["allocation_id"],
                row["promise_id"],
                row["payment_id"],
                float(row["allocated_amount"]),
                row["allocation_date"]
            ))

    print("Total payment allocation records loaded:", len(records))

    # Step 3: Insert or update records
    query = """
    INSERT INTO promise_payment_allocations (
        allocation_id,
        promise_id,
        payment_id,
        allocated_amount,
        allocation_date
    )
    VALUES (%s, %s, %s, %s, %s)

    ON DUPLICATE KEY UPDATE
        promise_id = VALUES(promise_id),
        payment_id = VALUES(payment_id),
        allocated_amount = VALUES(allocated_amount),
        allocation_date = VALUES(allocation_date)
    """

    cursor.executemany(query, records)

    # Step 4: Commit changes
    connection.commit()

    print("Payment allocation records processed:", cursor.rowcount)
    print("Promise payment allocations imported successfully!")

except Exception as error:

    if connection is not None and connection.is_connected():
        connection.rollback()

    print("Payment allocation import failed:", error)

finally:

    if cursor is not None:
        cursor.close()

    if connection is not None and connection.is_connected():
        connection.close()
        print("Database connection closed.")
