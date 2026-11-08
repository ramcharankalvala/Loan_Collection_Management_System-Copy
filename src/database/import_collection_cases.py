
import csv
from src.database.db_connection import get_connection

connection = None
cursor = None

try:
    # Step 1: Read collection cases from CSV
    records = []

    with open(
        "data/collection_cases.csv",
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            records.append((
                row["case_id"],
                row["loan_id"],
                row["customer_id"],
                int(row["priority_rank"]),
                int(row["priority_score"]),
                float(row["outstanding"]),
                int(row["dpd"]),
                row["case_status"],
                row["action_status"],
                row["dispute_status"],
                row["hardship_status"],
                row["contact_status"]
            ))

    print("Total collection case records loaded:", len(records))

    # Step 2: Connect to MySQL
    connection = get_connection()
    cursor = connection.cursor()

    # Step 3: Insert or update collection cases
    query = """
    INSERT INTO collection_cases (
        case_id, loan_id, customer_id, priority_rank,
        priority_score, outstanding, dpd, case_status,
        action_status, dispute_status, hardship_status,
        contact_status
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        loan_id = VALUES(loan_id),
        customer_id = VALUES(customer_id),
        priority_rank = VALUES(priority_rank),
        priority_score = VALUES(priority_score),
        outstanding = VALUES(outstanding),
        dpd = VALUES(dpd),
        case_status = VALUES(case_status),
        action_status = VALUES(action_status),
        dispute_status = VALUES(dispute_status),
        hardship_status = VALUES(hardship_status),
        contact_status = VALUES(contact_status)
    """

    cursor.executemany(query, records)
    connection.commit()

    print("Collection case records processed:", cursor.rowcount)
    print("Collection cases imported successfully!")

except Exception as error:

    if connection is not None and connection.is_connected():
        connection.rollback()

    print("Error importing collection cases:", error)

finally:

    if cursor is not None:
        cursor.close()

    if connection is not None and connection.is_connected():
        connection.close()
        print("Database connection closed.")
