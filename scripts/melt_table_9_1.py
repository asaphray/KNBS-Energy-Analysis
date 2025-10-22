import pandas as pd
import os

def clean_table_9_1(filepath):
    """
    Cleans and reshapes Table 9.1:
    Quantity and Value of Imports, Exports, and Re-Exports of Petroleum Products (2019–2023).
    """

    # Load CSV
    df = pd.read_csv(filepath)
    df = df.dropna(how="all").dropna(axis=1, how="all")

    # Rename first column if unnamed
    if df.columns[0].startswith("Unnamed"):
        df.columns.values[0] = "Category"

    # Forward-fill Category names (IMPORTS, EXPORTS, etc.)
    df["Category"] = df["Category"].ffill()

    # Find where "Value" section starts
    split_idx = df[df.iloc[:, 0].astype(str).str.contains("Value", case=False, na=False)].index
    if len(split_idx) == 0:
        raise ValueError("Couldn't find the 'Value' section in the first column.")
    split_idx = split_idx[0]

    # Split Quantity and Value sections
    df_quantity = df.iloc[:split_idx].copy()
    df_value = df.iloc[split_idx + 1 :].copy()

    # The first row after "Quantity..." is the header row (years)
    quantity_header = df_quantity.iloc[0].tolist()
    value_header = df_value.iloc[0].tolist()

    df_quantity.columns = quantity_header
    df_value.columns = value_header

    # Drop the header rows now in data
    df_quantity = df_quantity.iloc[1:]
    df_value = df_value.iloc[1:]

    # Standardize columns
    df_quantity.rename(columns={df_quantity.columns[0]: "Category", df_quantity.columns[1]: "Product"}, inplace=True)
    df_value.rename(columns={df_value.columns[0]: "Category", df_value.columns[1]: "Product"}, inplace=True)

    # Melt to long format
    quantity_cols = [c for c in df_quantity.columns if c not in ["Category", "Product"]]
    value_cols = [c for c in df_value.columns if c not in ["Category", "Product"]]

    df_q = df_quantity.melt(id_vars=["Category", "Product"], value_vars=quantity_cols, var_name="Year", value_name="Quantity")
    df_v = df_value.melt(id_vars=["Category", "Product"], value_vars=value_cols, var_name="Year", value_name="Value")

    # Merge
    merged = pd.merge(df_q, df_v, on=["Category", "Product", "Year"], how="inner")

    # Clean types
    merged["Year"] = merged["Year"].astype(str).str.extract(r"(\d{4})").astype(int)
    merged["Quantity"] = pd.to_numeric(merged["Quantity"], errors="coerce")
    merged["Value"] = pd.to_numeric(merged["Value"], errors="coerce")

    return merged


if __name__ == "__main__":
    DATA_DIR = "outputs/cleaned"
    FILENAME = "table_9_1_quantity_and_value_of_imports_exports_and_re_exports_of_petroleum_products_2019_2023.csv"
    filepath = os.path.join(DATA_DIR, FILENAME)

    tidy_df = clean_table_9_1(filepath)
    print(tidy_df.head(15))

    # Save
    tidy_df.to_csv(os.path.join(DATA_DIR, "tidy_table_9_1.csv"), index=False)
    print(f"\n✅ Cleaned data saved to {os.path.join(DATA_DIR, 'tidy_table_9_1.csv')}")
