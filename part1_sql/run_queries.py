import sqlite3
import csv
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "meesho_reseller.db"
OUTPUT_DIR = BASE_DIR / "part1_sql" / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

conn = sqlite3.connect(DB_PATH)

# Query 1
query1 = """
SELECT
    month,
    category,
    ROUND(SUM(quantity * unit_price), 2) AS revenue,
    COUNT(*) AS n_orders
FROM orders
GROUP BY month, category
ORDER BY
    CASE month
        WHEN 'April' THEN 1
        WHEN 'May' THEN 2
        WHEN 'June' THEN 3
    END,
    category;
"""

cursor = conn.execute(query1)
rows = cursor.fetchall()
columns = [description[0] for description in cursor.description]

output_file = OUTPUT_DIR / "monthly_category_revenue.csv"

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(columns)
    writer.writerows(rows)

    # Query 2
query2 = """
SELECT
    r.region,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS total_revenue,
    COUNT(*) AS n_orders
FROM orders o
JOIN resellers r
    ON o.reseller_id = r.reseller_id
GROUP BY r.region
ORDER BY total_revenue DESC;
"""

cursor = conn.execute(query2)
rows = cursor.fetchall()
columns = [description[0] for description in cursor.description]

output_file = OUTPUT_DIR / "region_revenue.csv"

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(columns)
    writer.writerows(rows)

print(f"Created: {output_file}")


# Query 3
query3 = """
SELECT
    o.reseller_id,
    r.reseller_name AS reseller_name,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS total_spend
FROM orders o
JOIN resellers r
    ON o.reseller_id = r.reseller_id
GROUP BY o.reseller_id, r.reseller_name
HAVING total_spend > 50000
ORDER BY total_spend DESC
LIMIT 5;
"""

cursor = conn.execute(query3)
rows = cursor.fetchall()
columns = [description[0] for description in cursor.description]

output_file = OUTPUT_DIR / "top_resellers.csv"

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(columns)
    writer.writerows(rows)

print(f"Created: {output_file}")


# Query 4
query4 = """
SELECT
    r.reseller_id,
    r.reseller_name AS reseller_name
FROM resellers r
LEFT JOIN orders o
    ON r.reseller_id = o.reseller_id
WHERE o.order_id IS NULL;
"""

cursor = conn.execute(query4)
rows = cursor.fetchall()
columns = [description[0] for description in cursor.description]

output_file = OUTPUT_DIR / "zero_order_resellers.csv"

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(columns)
    writer.writerows(rows)

print(f"Created: {output_file}")

# Query 4(b)
query4b = """
SELECT
    r.reseller_id,
    r.reseller_name AS reseller_name,
    COUNT(*) AS count_star,
    COUNT(o.order_id) AS count_order_id
FROM resellers r
LEFT JOIN orders o
    ON r.reseller_id = o.reseller_id
GROUP BY r.reseller_id, r.reseller_name
HAVING COUNT(o.order_id) = 0;
"""

cursor = conn.execute(query4b)
rows = cursor.fetchall()
columns = [description[0] for description in cursor.description]

output_file = OUTPUT_DIR / "zero_order_count_check.csv"

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(columns)
    writer.writerows(rows)

print(f"Created: {output_file}")

# Query 5
query5 = """
SELECT
    ROUND(
        SUM(quantity * unit_price) / COUNT(*),
        2
    ) AS june_delivered_aov
FROM orders
WHERE month = 'June'
  AND status = 'Delivered';
"""

cursor = conn.execute(query5)
rows = cursor.fetchall()
columns = [description[0] for description in cursor.description]

output_file = OUTPUT_DIR / "june_delivered_aov.csv"

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(columns)
    writer.writerows(rows)

print(f"Created: {output_file}")

conn.close()
