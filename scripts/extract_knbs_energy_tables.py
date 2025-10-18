"""
Extract and rename KNBS energy tables automatically using their in-sheet titles.
"""

import os
import pandas as pd
import re


def extract_titles_and_save(xlsx_path, output_dir="outputs/cleaned"):
    """
    Loads all sheets in a KNBS energy Excel file, extracts table titles,
    and saves each sheet as a CSV named after the title.

    Parameters
    ----------
    xlsx_path : str
        Path to the Excel file.
    output_dir : str
        Directory to save cleaned CSVs.
    """
    os.makedirs(output_dir, exist_ok=True)

    xls = pd.ExcelFile(xlsx_path)

    for sheet in xls.sheet_names:
        try:
            # Read first 5 rows only to get title
            header_df = pd.read_excel(xls, sheet_name=sheet, nrows=5, header=None)

            # Find first non-empty cell — often the title
            title = header_df.stack().iloc[0]
            title = str(title).strip()

            # Clean title → safe filename
            clean_name = re.sub(r'[^A-Za-z0-9]+', '_', title).strip('_').lower()

            # Load full table (after skipping title rows)
            df = pd.read_excel(xls, sheet_name=sheet, skiprows=5)

            # Save CSV
            output_path = os.path.join(output_dir, f"{clean_name}.csv")
            df.to_csv(output_path, index=False)

            print(f"✅ {sheet} → {clean_name}.csv")

        except Exception as e:
            print(f"⚠️ Skipped {sheet} due to error: {e}")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "data", "energy-tables18-23.xlsx")
    output_dir = os.path.join(base_dir, "outputs", "cleaned")

    extract_titles_and_save(data_path, output_dir)
