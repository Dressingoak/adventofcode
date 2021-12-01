import sqlite3
import pandas as pd

# Create database
conn = sqlite3.connect(":memory:")
conn.execute("""CREATE TABLE data (
    minimum INTEGER,
    maximum INTEGER,
    char TEXT,
    password TEXT
)""")

# Add data to table
data = pd.read_csv('input.txt', header=None)
data.columns = ["str"]
pattern = r'^(\d+)\-(\d+)\s+([a-z])\:\s+([a-z]+)$'
extracted = data["str"].str.extract(pattern, expand=True)
extracted.columns = ["minimum", "maximum", "char", "password"]
extracted.to_sql("data", conn, if_exists="append", index=False)

# Get result
conn.create_function('occurrences', 2, lambda s, x: s.count(x))

part1 = """SELECT
    COUNT(*) AS count
FROM (
    SELECT
        minimum,
        maximum,
        occurrences(password, char) AS occurrences
    FROM data
    WHERE minimum <= occurrences AND occurrences <= maximum
)
"""
(result1, ) = conn.execute(part1).fetchone()
print("Part 1: {}".format(result1))

part2 = """SELECT
    COUNT(*) AS count
FROM (
    SELECT
        substr(password, minimum, 1) AS first,
        substr(password, maximum, 1) AS second
    FROM data
    WHERE (first = char AND second != char) OR (first != char AND second = char)
)
"""
(result2, ) = conn.execute(part2).fetchone()
print("Part 2: {}".format(result2))
