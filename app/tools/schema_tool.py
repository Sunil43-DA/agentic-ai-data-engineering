import pandas as pd


def analyse_schema(file_path: str) -> dict:
    """
    Analyse the structure and basic quality of a CSV dataset.
    """

    df = pd.read_csv(file_path)

    profile = {
        "file": file_path,
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": df.columns.tolist(),
        "data_types": df.dtypes.astype(str).to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
        "duplicate_rows": int(df.duplicated().sum())
    }

    return profile