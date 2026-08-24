import os
import sqlite3

import pandas as pd


# ==================================================
# Database Configuration
# ==================================================

DATABASE_DIR = "data/database"

DATABASE_FILE = os.path.join(
    DATABASE_DIR,
    "customer.db"
)


# ==================================================
# Create Database Directory
# ==================================================

os.makedirs(
    DATABASE_DIR,
    exist_ok=True
)


# ==================================================
# Load Cleaned Data into SQLite
# ==================================================

def load_customers_to_database(
    csv_file: str
):

    # ----------------------------------------------
    # Read cleaned CSV
    # ----------------------------------------------

    df = pd.read_csv(
        csv_file
    )

    # ----------------------------------------------
    # Connect to SQLite
    # ----------------------------------------------

    connection = sqlite3.connect(
        DATABASE_FILE
    )

    try:

        # ------------------------------------------
        # Write data to customers table
        # ------------------------------------------

        df.to_sql(
            "customers",
            connection,
            if_exists="replace",
            index=False
        )

        # ------------------------------------------
        # Verify row count
        # ------------------------------------------

        cursor = connection.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM customers"
        )

        row_count = cursor.fetchone()[0]

        return {
            "database": DATABASE_FILE,
            "table": "customers",
            "rows_loaded": row_count,
            "status": "success"
        }

    finally:

        connection.close()

# ==================================================
# SQL Validation
# ==================================================

def validate_customer_database():

    connection = sqlite3.connect(
        DATABASE_FILE
    )

    try:

        cursor = connection.cursor()

        # ------------------------------------------
        # Total customer records
        # ------------------------------------------

        cursor.execute(
            "SELECT COUNT(*) FROM customers"
        )

        total_rows = cursor.fetchone()[0]

        # ------------------------------------------
        # Missing emails
        # ------------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM customers
            WHERE email IS NULL
               OR TRIM(email) = ''
            """
        )

        missing_emails = cursor.fetchone()[0]

        # ------------------------------------------
        # Invalid ages
        # ------------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM customers
            WHERE age IS NULL
               OR age < 18
               OR age > 100
            """
        )

        invalid_ages = cursor.fetchone()[0]

        # ------------------------------------------
        # Duplicate customer IDs
        # ------------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM (
                SELECT customer_id
                FROM customers
                GROUP BY customer_id
                HAVING COUNT(*) > 1
            )
            """
        )

        duplicate_ids = cursor.fetchone()[0]

        # ------------------------------------------
        # Return validation result
        # ------------------------------------------

        return {
            "total_rows": total_rows,
            "missing_emails": missing_emails,
            "invalid_ages": invalid_ages,
            "duplicate_customer_ids": duplicate_ids,
            "status": "valid"
            if (
                missing_emails == 0
                and invalid_ages == 0
                and duplicate_ids == 0
            )
            else "invalid"
        }

    finally:

        connection.close()