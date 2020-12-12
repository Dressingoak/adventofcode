import sqlite3
import pandas as pd

# Create database
conn = sqlite3.connect(":memory:")
conn.execute("""CREATE TABLE data (value INTEGER);""")

# Add data to table
data = pd.read_csv('data.txt', header=None)
data.columns = ["value"]
data.to_sql("data", conn, if_exists="append", index=False)

# Get result
query = """SELECT
    left.value + right.value AS sum,
    left.value * right.value AS prod
FROM data AS left
JOIN data AS right ON left.rowid < right.rowid
WHERE sum = 2020
"""
(_, result) = conn.execute(query).fetchone()
print(result)
