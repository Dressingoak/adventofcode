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
    first.value + second.value + third.value AS sum,
    first.value * second.value * third.value AS prod
FROM data AS first
JOIN data AS second ON first.rowid < second.rowid
JOIN data AS third ON second.rowid < third.rowid
WHERE sum = 2020
"""
(_, result) = conn.execute(query).fetchone()
print(result)
