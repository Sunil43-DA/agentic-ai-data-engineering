import pandas as pd


def check_data_quality(file_path: str) -> dict:
    """
    Run deterministic data-quality checks on a customer dataset.
    """

    df = pd.read_csv(file_path)

    missing_values = df.isnull().sum()
    missing_values = {
        column: int(count)
        for column, count in missing_values.items()
        if count > 0
    }

    duplicate_rows = int(df.duplicated().sum())

    duplicate_customer_ids = int(
        df["customer_id"].duplicated().sum()
    )

    invalid_age_count = int(
        ((df["age"] < 0) | (df["age"] > 120)).fillna(False).sum()
    )

    email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    invalid_email_count = int(
        (
            ~df["email"].fillna("").str.match(email_pattern)
        ).sum()
    )

    return {
        "missing_values": missing_values,
        "duplicate_rows": duplicate_rows,
        "duplicate_customer_ids": duplicate_customer_ids,
        "invalid_age_count": invalid_age_count,
        "invalid_email_count": invalid_email_count
    }


if __name__ == "__main__":
    result = check_data_quality("data/raw/customer.csv")

    print("\n===== DATA QUALITY RESULTS =====")
    print(result)