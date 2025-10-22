"""
Exploratory Analysis for Table 9.1:
Quantity and Value of Imports, Exports, and Re-Exports of Petroleum Products (2019–2023)
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configuring visualization style
sns.set_theme(style="whitegrid", palette="Set2")

# File path
DATA_DIR = os.path.join("outputs", "cleaned")
FILENAME = "table_9_1_quantity_and_value_of_imports_exports_and_re_exports_of_petroleum_products_2019_2023.csv"
filepath = os.path.join(DATA_DIR, FILENAME)

# Load dataset
df = pd.read_csv(filepath)

# Basic Info 
print("\n✅ Loaded Successfully!")
print(f"Shape: {df.shape}")
print("\n📋 Columns:")
print(df.columns.tolist())

print("\n🔍 Data Types:")
print(df.dtypes)

print("\n🧹 Missing Values:")
print(df.isna().sum())

#  A glimpse
print("\n🔎 Sample Rows:")
print(df.head())

#  Summary Stats 
print("\n📈 Summary Statistics:")
print(df.describe())

#  Optional Visualization 
plt.figure(figsize=(10, 5))
sns.heatmap(df.isna(), cbar=False)
plt.title("Missing Data Heatmap")
plt.show()
