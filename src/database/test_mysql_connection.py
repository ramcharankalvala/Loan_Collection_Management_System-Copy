from db_connection import get_connection

connection = None

try:
    connection = get_connection()

    if connection.is_connected():
        print("MySQL connection successful!")
        print("Database:", connection.database)

except Exception as error:
    print("Database connection failed:", error)

finally:
    if connection is not None and connection.is_connected():
        connection.close()
        print("Database connection closed.")