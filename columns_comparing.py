# -*- coding: utf-8 -*-
"""Columns_comparing.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1mJAYJ7O-3wCckieQ1e1_SCleP9mOO2UJ
"""

import pandas as pd

# Sample data for the columns
col1 = ["Next Up, Feed - Explore More, WP Right Rail (primary-widget-area-2), taboola-vignette, Feed - Below Article Thumbnails, Mid Article Thumbnails","Next Up, Feed - Explore More, Right Rail Thumbnails, Feed - Below Article Thumbnails, taboola-vignette, Feed - Below Article Thumbnails AMP, Right Rail Thumbnails AMP","Feed - Below Article Thumbnails, Feed - Explore More","Feed - Below Article Thumbnails, Feed - Explore More","Feed - Below Article Thumbnails, taboola-vignette, Next Up, Mid Article Thumbnails, Feed - Explore More"]

col2 = ["Feed - Below Article Thumbnails, Next Up, Mid Article Thumbnails, Feed - Explore More, WP Right Rail (primary-widget-area-2), taboola-vignette","Feed - Explore More, Next Up, Feed - Below Article Thumbnails, taboola-vignette, Right Rail Thumbnails, Feed - Below Article Thumbnails AMP","Feed - Below Article Thumbnails, Feed - Explore More","Feed - Below Article Thumbnails, Feed - Explore More","taboola-vignette, Feed - Explore More, Feed - Below Article Thumbnails, Next Up, Mid Article Thumbnails"]

# Function to compare two columns row-by-row
def compare_columns(col1, col2):
    results = []
    for i, (row1, row2) in enumerate(zip(col1, col2), start=1):
        # Split values into sets for comparison
        set1 = set(row1.split(", "))
        set2 = set(row2.split(", "))

        # Find unique values in each row
        unique_to_col1 = set1 - set2  # Values in col1 but not in col2
        unique_to_col2 = set2 - set1  # Values in col2 but not in col1

        # Append the result for the row
        results.append({
            "Row": i,
            "Unique to Col1": unique_to_col1,
            "Unique to Col2": unique_to_col2
        })

    return results

# Compare the columns and get the differences
differences = compare_columns(col1, col2)

# Convert the results to a Pandas DataFrame for table display
df = pd.DataFrame(differences)

# Display the DataFrame
df.set_index("Row", inplace=True)
df["Unique to Col1"] = df["Unique to Col1"].apply(lambda x: ', '.join(x) if x else 'None')
df["Unique to Col2"] = df["Unique to Col2"].apply(lambda x: ', '.join(x) if x else 'None')

# Display the table
df