
from src.database.db_connection import get_connection
import csv

connection = None
cursor = None

try:
    # Step 1: Connect to MySQL
    connection = get_connection()
    cursor = connection.cursor()

    # Step 2: Read collection priority CSV
    records = []

    with open(
        "data/collection_priority.csv",
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            records.append((
                int(row["priority_rank"]),
                row["loan_id"],
                int(row["priority_score"]),
                float(row["outstanding"]),
                int(row["dpd"]),
                int(row["risk_score"]),
                int(row["balance_score"]),
                int(row["dpd_score"]),
                row["hardship_flag"].lower() == "true",
                row["dispute_flag"].lower() == "true",
                row["contact_restricted"].lower() == "true",
                row["dispute_status"],
                row["hardship_status"],
                row["contact_status"],
                row["action_status"]
            ))

    print("Total priority records loaded:", len(records))

    # Step 3: Insert or update records
    query = """
    INSERT INTO collection_priority (
        priority_rank,
        loan_id,
        priority_score,
        outstanding,
        dpd,
        risk_score,
        balance_score,
        dpd_score,
        hardship_flag,
        dispute_flag,
        contact_restricted,
        dispute_status,
        hardship_status,
        contact_status,
        action_status
    )
    VALUES (
        %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s
    )

    ON DUPLICATE KEY UPDATE
        priority_rank = VALUES(priority_rank),
        priority_score = VALUES(priority_score),
        outstanding = VALUES(outstanding),
        dpd = VALUES(dpd),
        risk_score = VALUES(risk_score),
        balance_score = VALUES(balance_score),
        dpd_score = VALUES(dpd_score),
        hardship_flag = VALUES(hardship_flag),
        dispute_flag = VALUES(dispute_flag),
        contact_restricted = VALUES(contact_restricted),
        dispute_status = VALUES(dispute_status),
        hardship_status = VALUES(hardship_status),
        contact_status = VALUES(contact_status),
        action_status = VALUES(action_status)
    """

    cursor.executemany(query, records)

    # Step 4: Commit transaction
    connection.commit()

    print("Priority records processed:", cursor.rowcount)
    print("Collection priority imported successfully!")

except Exception as error:

    if connection is not None and connection.is_connected():
        connection.rollback()

    print("Priority import failed:", error)

finally:

    if cursor is not None:
        cursor.close()

    if connection is not None and connection.is_connected():
        connection.close()
        print("Database connection closed.")
