import sqlite3
import pandas as pd

# Create database
conn = sqlite3.connect(":memory:")
conn.execute("""CREATE TABLE data (
    level TEXT,
    position INTEGER
)""")

# Add data to table
data = pd.read_csv('input.txt', header=None)
data.columns = ["str"]
pattern = r'^([\.#]+)$'
extracted = data["str"].str.extract(pattern)
extracted.columns = ["level"]
extracted["position"] = extracted.index
extracted.to_sql("data", conn, if_exists="append", index=False)

part1 = """
SELECT
    value,
    COUNT(*) as `count`
FROM (
    SELECT
        *,
        SUBSTR(level, col, 1) AS value
    FROM (
        SELECT
            level,
            (position * 3) % LENGTH(level) + 1 AS col
        FROM data
        WHERE position > 0
    )
)
GROUP BY value
HAVING value = '#'
"""
(_, result1) = conn.execute(part1).fetchone()
print("Part 1: {}".format(result1))

conn.execute("""CREATE TABLE slopes (right INTEGER, down INTEGER)""")
conn.execute("""INSERT INTO slopes (right, down) VALUES
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2)
""")

class Product:
    def __init__(self):
        self.prod = 1

    def step(self, value):
        self.prod *= value

    def finalize(self):
        return self.prod

conn.create_aggregate("prod", 1, Product)

part2 = """
SELECT
    PROD(`count`) AS product
FROM (
    SELECT
        right,
        down,
        value,
        SUM(value) as `count`
    FROM (
        SELECT
            *,
            SUBSTR(level, col, 1) = '#' AS value
        FROM (
            SELECT
                right,
                down,
                level,
                (position * right) % LENGTH(level) + 1 AS col
            FROM data
            CROSS JOIN slopes
            WHERE position > 0 AND position % down = 0
        )
    )
    GROUP BY right, down
)
"""

(result2, ) = conn.execute(part2).fetchone()
print("Part 2 (incorrect): {}".format(result2))
