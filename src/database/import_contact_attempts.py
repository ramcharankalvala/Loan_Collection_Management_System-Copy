
import csv
from src.database.db_connection import get_connection

connection = None
cursor = None

try:
    # Step 1: Connect to MySQL
    connection = get_connection()
    cursor = connection.cursor()

    # Step 2: Read contact attempt records
    records = []

    with open(
        "data/contact_attempts.csv",
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            records.append((
                row["attempt_id"],
                row["case_id"],
                row["loan_id"],
                row["customer_id"],
                row["attempt_datetime"],
                row["channel"],
                row["outcome"],
                row["data_source"]
            ))

    print("Total contact attempt records loaded:", len(records))

    # Step 3: Insert or update records
    query = """
    INSERT INTO contact_attempts (
        attempt_id,
        case_id,
        loan_id,
        customer_id,
        attempt_datetime,
        channel,
        outcome,
        data_source
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)

    ON DUPLICATE KEY UPDATE
        case_id = VALUES(case_id),
        loan_id = VALUES(loan_id),
        customer_id = VALUES(customer_id),
        attempt_datetime = VALUES(attempt_datetime),
        channel = VALUES(channel),
        outcome = VALUES(outcome),
        data_source = VALUES(data_source)
    """

    cursor.executemany(query, records)

    # Step 4: Commit changes
    connection.commit()

    print("Contact attempt records processed:", cursor.rowcount)
    print("Contact attempts imported successfully!")

except Exception as error:

    if connection is not None and connection.is_connected():
        connection.rollback()

    print("Contact attempt import failed:", error)

finally:

    if cursor is not None:
        cursor.close()

    if connection is not None and connection.is_connected():
        connection.close()
        print("Database connection closed.")
