
import mysql.connector
from getpass import getpass


def get_connection():

    password = getpass("Enter MySQL password: ")

    connection = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password=password,
        database="loan_collection_db"
    )

    return connection
