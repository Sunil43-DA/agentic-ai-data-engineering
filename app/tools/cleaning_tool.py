import os

import pandas as pd


def clean_customer_data(
    input_path: str,
    output_path: str
) -> dict:
    """
    Clean the customer dataset and save the cleaned version.
    """

    df = pd.read_csv(input_path)

    original_rows = len(df)

    # 1. Remove exact duplicate rows
    duplicate_rows_removed = int(df.duplicated().sum())

    df = df.drop_duplicates()

    # 2. Convert age to numeric
    df["age"] = pd.to_numeric(
        df["age"],
        errors="coerce"
    )

    # 3. Detect invalid ages
    invalid_age_mask = (
        (df["age"] < 0) |
        (df["age"] > 120)
    )

    invalid_age_count = int(
        invalid_age_mask.sum()
    )

    # Convert invalid ages to missing values
    df.loc[invalid_age_mask, "age"] = pd.NA

    # 4. Handle missing age values
    missing_age_count = int(
        df["age"].isna().sum()
    )

    if missing_age_count > 0:
        median_age = df["age"].median()

        df["age"] = df["age"].fillna(
            median_age
        )

    # 5. Clean email values
    missing_email_count = int(
        df["email"].isna().sum()
    )

    df["email"] = (
        df["email"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    # Handle missing emails
    df["email"] = df["email"].fillna(
        "unknown@example.com"
    )

    # 6. Convert age to integer
    df["age"] = df["age"].round().astype(int)

    # 7. Create output directory if needed
    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True
    )

    # 8. Save cleaned dataset
    df.to_csv(
        output_path,
        index=False
    )

    # 9. Return cleaning summary
    return {
        "input_file": input_path,
        "output_file": output_path,
        "original_rows": original_rows,
        "final_rows": len(df),
        "duplicate_rows_removed": duplicate_rows_removed,
        "invalid_ages_handled": invalid_age_count,
        "missing_age_handled": missing_age_count,
        "missing_email_handled": missing_email_count
    }


if __name__ == "__main__":

    result = clean_customer_data(
        "data/raw/customer.csv",
        "data/clean/customer_cleaned.csv"
    )

    print("\n===== CLEANING RESULTS =====")
    print(result)