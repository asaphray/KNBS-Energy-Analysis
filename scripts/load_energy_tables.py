import pandas as pd
import os


def load_energy_tables(filename="energy-tables18-23.xlsx", data_dir="../data"):
    """
    Load energy tables Excel file from the data directory.
    """
    filepath = os.path.join(os.path.dirname(__file__), data_dir, filename)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"The file '{filename}' was not found at '{filepath}'.")

    return pd.ExcelFile(filepath)


# ✅ Use the function to load the dataset
knbs_energy_tables = load_energy_tables()

# ✅ List available sheets
print(knbs_energy_tables.sheet_names)
# ✅ Load a specific sheet into a DataFrame
