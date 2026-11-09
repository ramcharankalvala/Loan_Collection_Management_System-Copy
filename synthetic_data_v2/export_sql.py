
import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
DATABASE = "loan_collection_synthetic"

# Exact CSV columns and MySQL data types.
SCHEMAS = {
    "customers": [
        ("customer_id", "VARCHAR(40)"),
        ("name", "VARCHAR(150)"),
        ("email", "VARCHAR(255)"),
        ("city", "VARCHAR(100)"),
        ("phone", "VARCHAR(30)"),
    ],
    "accounts": [
        ("account_id", "VARCHAR(40)"),
        ("customer_id", "VARCHAR(40)"),
        ("account_status", "VARCHAR(40)"),
        ("opened_date", "DATE"),
        ("closed_date", "DATE"),
    ],
    "loans": [
        ("loan_id", "VARCHAR(40)"),
        ("account_id", "VARCHAR(40)"),
        ("customer_id", "VARCHAR(40)"),
        ("loan_amount", "DECIMAL(14,2)"),
        ("annual_interest_rate", "DECIMAL(7,4)"),
        ("loan_date", "DATE"),
        ("maturity_date", "DATE"),
    ],
    "installments": [
        ("installment_id", "VARCHAR(80)"),
        ("loan_id", "VARCHAR(40)"),
        ("customer_id", "VARCHAR(40)"),
        ("installment_number", "INT"),
        ("due_date", "DATE"),
        ("installment_amount", "DECIMAL(14,2)"),
    ],
    "payments": [
        ("payment_id", "VARCHAR(40)"),
        ("loan_id", "VARCHAR(40)"),
        ("customer_id", "VARCHAR(40)"),
        ("installment_id", "VARCHAR(80)"),
        ("installment_number", "INT"),
        ("payment_date", "DATE"),
        ("amount_due", "DECIMAL(14,2)"),
        ("amount_paid", "DECIMAL(14,2)"),
        ("payment_status", "VARCHAR(40)"),
    ],
    "delinquency_snapshots": [
        ("snapshot_id", "VARCHAR(40)"),
        ("loan_id", "VARCHAR(40)"),
        ("installment_id", "VARCHAR(80)"),
        ("as_of_date", "DATE"),
        ("due_date", "DATE"),
        ("amount_due", "DECIMAL(14,2)"),
        ("amount_paid", "DECIMAL(14,2)"),
        ("outstanding_amount", "DECIMAL(14,2)"),
        ("days_past_due", "INT"),
        ("installment_status", "VARCHAR(40)"),
    ],
    "contact_preferences": [
        ("customer_id", "VARCHAR(40)"),
        ("phone_allowed", "BOOLEAN"),
        ("sms_allowed", "BOOLEAN"),
        ("email_allowed", "BOOLEAN"),
        ("contact_opt_out", "BOOLEAN"),
        ("allowed_start_time", "TIME"),
        ("allowed_end_time", "TIME"),
    ],
    "collection_cases": [
        ("case_id", "VARCHAR(40)"),
        ("loan_id", "VARCHAR(40)"),
        ("account_id", "VARCHAR(40)"),
        ("customer_id", "VARCHAR(40)"),
        ("outstanding", "DECIMAL(14,2)"),
        ("days_past_due", "INT"),
        ("risk_score", "INT"),
        ("priority_score", "INT"),
        ("priority_rank", "INT"),
        ("case_status", "VARCHAR(50)"),
        ("action_status", "VARCHAR(60)"),
        ("dispute_status", "VARCHAR(50)"),
        ("hardship_status", "VARCHAR(50)"),
        ("contact_status", "VARCHAR(50)"),
    ],
    "risk_indicators": [
        ("loan_id", "VARCHAR(40)"),
        ("missed_installments", "INT"),
        ("days_past_due", "INT"),
        ("hardship_flag", "BOOLEAN"),
        ("dispute_flag", "BOOLEAN"),
        ("contact_restricted", "BOOLEAN"),
        ("risk_score", "INT"),
    ],
    "contact_attempts": [
        ("attempt_id", "VARCHAR(80)"),
        ("case_id", "VARCHAR(40)"),
        ("loan_id", "VARCHAR(40)"),
        ("customer_id", "VARCHAR(40)"),
        ("attempt_datetime", "DATETIME"),
        ("channel", "VARCHAR(40)"),
        ("outcome", "VARCHAR(60)"),
        ("within_allowed_window", "BOOLEAN"),
    ],
    "promises_to_pay": [
        ("promise_id", "VARCHAR(40)"),
        ("case_id", "VARCHAR(40)"),
        ("loan_id", "VARCHAR(40)"),
        ("customer_id", "VARCHAR(40)"),
        ("promise_amount", "DECIMAL(14,2)"),
        ("created_date", "DATE"),
        ("promise_date", "DATE"),
        ("amount_paid", "DECIMAL(14,2)"),
        ("remaining_amount", "DECIMAL(14,2)"),
        ("promise_status", "VARCHAR(40)"),
    ],
    "ground_truth": [
        ("record_id", "VARCHAR(100)"),
        ("entity", "VARCHAR(60)"),
        ("anomaly_type", "VARCHAR(100)"),
        ("expected_decision", "VARCHAR(100)"),
    ],
}

PRIMARY_KEYS = {
    "customers": "customer_id",
    "accounts": "account_id",
    "loans": "loan_id",
    "installments": "installment_id",
    "payments": "payment_id",
    "delinquency_snapshots": "snapshot_id",
    "contact_preferences": "customer_id",
    "collection_cases": "case_id",
    "risk_indicators": "loan_id",
    "contact_attempts": "attempt_id",
    "promises_to_pay": "promise_id",
    "ground_truth": "record_id",
}

FOREIGN_KEYS = {
    "accounts": [
        ("customer_id", "customers", "customer_id"),
    ],
    "loans": [
        ("account_id", "accounts", "account_id"),
        ("customer_id", "customers", "customer_id"),
    ],
    "installments": [
        ("loan_id", "loans", "loan_id"),
        ("customer_id", "customers", "customer_id"),
    ],
    "payments": [
        ("loan_id", "loans", "loan_id"),
        ("customer_id", "customers", "customer_id"),
        ("installment_id", "installments", "installment_id"),
    ],
    "delinquency_snapshots": [
        ("loan_id", "loans", "loan_id"),
        ("installment_id", "installments", "installment_id"),
    ],
    "contact_preferences": [
        ("customer_id", "customers", "customer_id"),
    ],
    "collection_cases": [
        ("loan_id", "loans", "loan_id"),
        ("account_id", "accounts", "account_id"),
        ("customer_id", "customers", "customer_id"),
    ],
    "risk_indicators": [
        ("loan_id", "loans", "loan_id"),
    ],
    "contact_attempts": [
        ("case_id", "collection_cases", "case_id"),
        ("loan_id", "loans", "loan_id"),
        ("customer_id", "customers", "customer_id"),
    ],
    "promises_to_pay": [
        ("case_id", "collection_cases", "case_id"),
        ("loan_id", "loans", "loan_id"),
        ("customer_id", "customers", "customer_id"),
    ],
}

# Parent tables are created and populated before child tables.
TABLE_ORDER = [
    "customers",
    "accounts",
    "loans",
    "installments",
    "contact_preferences",
    "payments",
    "delinquency_snapshots",
    "collection_cases",
    "risk_indicators",
    "contact_attempts",
    "promises_to_pay",
    "ground_truth",
]

BOOLEAN_FIELDS = {
    "phone_allowed",
    "sms_allowed",
    "email_allowed",
    "contact_opt_out",
    "hardship_flag",
    "dispute_flag",
    "contact_restricted",
    "within_allowed_window",
}


def sql_value(value, column, sql_type):
    if value is None or value == "":
        return "NULL"

    if column in BOOLEAN_FIELDS:
        return "1" if value.strip().lower() in ("true", "1", "yes") else "0"

    if sql_type.startswith(("INT", "DECIMAL")):
        return value

    escaped = value.replace("\\", "\\\\").replace("'", "''")
    return "'" + escaped + "'"


def create_schema():
    lines = [
        f"CREATE DATABASE IF NOT EXISTS `{DATABASE}`;",
        f"USE `{DATABASE}`;",
        "",
        "SET FOREIGN_KEY_CHECKS = 0;",
    ]

    # Drop child tables before parent tables.
    for table in reversed(TABLE_ORDER):
        lines.append(f"DROP TABLE IF EXISTS `{table}`;")

    lines.extend(["", "SET FOREIGN_KEY_CHECKS = 1;", ""])

    for table in TABLE_ORDER:
        definitions = []

        for column, sql_type in SCHEMAS[table]:
            nullability = (
                "NOT NULL"
                if column == PRIMARY_KEYS[table]
                else "NULL"
            )
            definitions.append(
                f"    `{column}` {sql_type} {nullability}"
            )

        primary_key = PRIMARY_KEYS[table]
        definitions.append(
            f"    PRIMARY KEY (`{primary_key}`)"
        )

        for column, parent_table, parent_column in FOREIGN_KEYS.get(
            table, []
        ):
            constraint = f"fk_{table}_{column}"
            definitions.append(
                f"    CONSTRAINT `{constraint}` "
                f"FOREIGN KEY (`{column}`) "
                f"REFERENCES `{parent_table}` (`{parent_column}`)"
            )

        lines.append(f"CREATE TABLE `{table}` (")
        lines.append(",\n".join(definitions))
        lines.append(
            ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"
        )
        lines.append("")

    schema_path = OUTPUT_DIR / "schema.sql"
    schema_path.write_text("\n".join(lines), encoding="utf-8")
    print("Created:", schema_path)


def export_seed_data():
    lines = [
        f"USE `{DATABASE}`;",
        "",
        "SET FOREIGN_KEY_CHECKS = 1;",
        "",
    ]

    total_rows = 0

    for table in TABLE_ORDER:
        csv_path = OUTPUT_DIR / f"{table}.csv"

        if not csv_path.exists():
            raise FileNotFoundError(
                f"Missing CSV file: {csv_path}"
            )

        columns = [
            column for column, sql_type in SCHEMAS[table]
        ]
        types = dict(SCHEMAS[table])

        with csv_path.open(
            "r", newline="", encoding="utf-8-sig"
        ) as file:
            reader = csv.DictReader(file)

            if reader.fieldnames != columns:
                raise ValueError(
                    f"Column mismatch in {csv_path.name}\n"
                    f"Expected: {columns}\n"
                    f"Found: {reader.fieldnames}"
                )

            batch = []
            table_rows = 0

            for row in reader:
                values = [
                    sql_value(
                        row[column], column, types[column]
                    )
                    for column in columns
                ]

                batch.append("(" + ", ".join(values) + ")")
                total_rows += 1
                table_rows += 1

                if len(batch) == 500:
                    column_list = ", ".join(
                        f"`{column}`" for column in columns
                    )
                    lines.append(
                        f"INSERT INTO `{table}` "
                        f"({column_list}) VALUES"
                    )
                    lines.append(",\n".join(batch) + ";")
                    lines.append("")
                    batch = []

            if batch:
                column_list = ", ".join(
                    f"`{column}`" for column in columns
                )
                lines.append(
                    f"INSERT INTO `{table}` "
                    f"({column_list}) VALUES"
                )
                lines.append(",\n".join(batch) + ";")
                lines.append("")

        print(f"Exported {table}: {table_rows} rows")

    seed_path = OUTPUT_DIR / "seed_data.sql"
    seed_path.write_text("\n".join(lines), encoding="utf-8")

    print("\nCreated:", seed_path)
    print("Total SQL records:", total_rows)


if __name__ == "__main__":
    if not OUTPUT_DIR.exists():
        raise FileNotFoundError(
            f"Output directory not found: {OUTPUT_DIR}"
        )

    create_schema()
    export_seed_data()

    print("\nSQL EXPORT COMPLETED")
