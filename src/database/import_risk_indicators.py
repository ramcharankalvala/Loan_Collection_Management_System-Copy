
import csv
from src.database.db_connection import get_connection

connection = None
cursor = None

try:
    # Step 1: Connect to MySQL
    connection = get_connection()
    cursor = connection.cursor()

    # Step 2: Read risk indicator records
    risk_records = []

    with open(
        "data/risk_indicators.csv",
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            risk_records.append((
                row["loan_id"],
                int(row["missed_installments"]),
                row["repeated_payment_failure"].lower() == "true",
                row["hardship_flag"].lower() == "true",
                row["dispute_flag"].lower() == "true",
                row["contact_restricted"].lower() == "true",
                int(row["risk_score"]),
                row["data_source"]
            ))

    print("Total risk records loaded:", len(risk_records))

    # Step 3: Insert or update records in MySQL
    query = """
    INSERT INTO risk_indicators (
        loan_id,
        missed_installments,
        repeated_payment_failure,
        hardship_flag,
        dispute_flag,
        contact_restricted,
        risk_score,
        data_source
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)

    ON DUPLICATE KEY UPDATE
        missed_installments = VALUES(missed_installments),
        repeated_payment_failure = VALUES(repeated_payment_failure),
        hardship_flag = VALUES(hardship_flag),
        dispute_flag = VALUES(dispute_flag),
        contact_restricted = VALUES(contact_restricted),
        risk_score = VALUES(risk_score),
        data_source = VALUES(data_source)
    """

    cursor.executemany(query, risk_records)

    # Step 4: Save changes
    connection.commit()

    print("Risk records processed:", cursor.rowcount)
    print("Risk indicators imported successfully!")

except Exception as error:

    if connection is not None and connection.is_connected():
        connection.rollback()

    print("Risk import failed:", error)

finally:

    if cursor is not None:
        cursor.close()

    if connection is not None and connection.is_connected():
        connection.close()
        print("Database connection closed.")
