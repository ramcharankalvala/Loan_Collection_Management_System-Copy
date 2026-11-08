
import csv
from src.database.db_connection import get_connection

connection = None
cursor = None

try:
    # Step 1: Connect to MySQL
    connection = get_connection()
    cursor = connection.cursor()

    # Step 2: Read contact preference records
    records = []

    with open(
        "data/contact_preferences.csv",
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            records.append((
                row["customer_id"],
                row["phone_allowed"].lower() == "true",
                row["sms_allowed"].lower() == "true",
                row["email_allowed"].lower() == "true",
                row["contact_opt_out"].lower() == "true",
                row["allowed_start_time"],
                row["allowed_end_time"],
                row["data_source"]
            ))

    print("Total contact preference records loaded:", len(records))

    # Step 3: Insert or update records
    query = """
    INSERT INTO contact_preferences (
        customer_id,
        phone_allowed,
        sms_allowed,
        email_allowed,
        contact_opt_out,
        allowed_start_time,
        allowed_end_time,
        data_source
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)

    ON DUPLICATE KEY UPDATE
        phone_allowed = VALUES(phone_allowed),
        sms_allowed = VALUES(sms_allowed),
        email_allowed = VALUES(email_allowed),
        contact_opt_out = VALUES(contact_opt_out),
        allowed_start_time = VALUES(allowed_start_time),
        allowed_end_time = VALUES(allowed_end_time),
        data_source = VALUES(data_source)
    """

    cursor.executemany(query, records)

    # Step 4: Commit changes
    connection.commit()

    print("Contact preference records processed:", cursor.rowcount)
    print("Contact preferences imported successfully!")

except Exception as error:

    if connection is not None and connection.is_connected():
        connection.rollback()

    print("Contact preference import failed:", error)

finally:

    if cursor is not None:
        cursor.close()

    if connection is not None and connection.is_connected():
        connection.close()
        print("Database connection closed.")
