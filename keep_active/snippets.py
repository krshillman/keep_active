"""
Code snippets for coding mode.

Provides a collection of realistic SQL and Python code snippets
that are typed out to simulate active coding.
"""

import random

SQL_SNIPPETS = [
    """\
SELECT u.id, u.username, u.email, COUNT(o.id) AS order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at >= '2025-01-01'
GROUP BY u.id, u.username, u.email
HAVING COUNT(o.id) > 5
ORDER BY order_count DESC
LIMIT 25;
""",
    """\
WITH monthly_revenue AS (
    SELECT
        DATE_TRUNC('month', order_date) AS month,
        SUM(total_amount) AS revenue,
        COUNT(DISTINCT customer_id) AS unique_customers
    FROM orders
    WHERE status = 'completed'
    GROUP BY DATE_TRUNC('month', order_date)
)
SELECT
    month,
    revenue,
    unique_customers,
    LAG(revenue) OVER (ORDER BY month) AS prev_month_revenue,
    ROUND((revenue - LAG(revenue) OVER (ORDER BY month)) / LAG(revenue) OVER (ORDER BY month) * 100, 2) AS growth_pct
FROM monthly_revenue
ORDER BY month DESC;
""",
    """\
CREATE TABLE IF NOT EXISTS audit_log (
    id SERIAL PRIMARY KEY,
    table_name VARCHAR(128) NOT NULL,
    record_id INTEGER NOT NULL,
    action VARCHAR(10) NOT NULL CHECK (action IN ('INSERT', 'UPDATE', 'DELETE')),
    old_values JSONB,
    new_values JSONB,
    changed_by INTEGER REFERENCES users(id),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_log_table ON audit_log(table_name, record_id);
CREATE INDEX idx_audit_log_changed_at ON audit_log(changed_at);
""",
    """\
UPDATE products p
SET
    stock_quantity = p.stock_quantity - oi.quantity,
    last_updated = NOW()
FROM order_items oi
JOIN orders o ON oi.order_id = o.id
WHERE oi.product_id = p.id
    AND o.status = 'confirmed'
    AND o.confirmed_at >= NOW() - INTERVAL '1 hour'
    AND p.stock_quantity >= oi.quantity;
""",
    """\
SELECT
    d.department_name,
    e.employee_id,
    e.full_name,
    e.salary,
    RANK() OVER (PARTITION BY d.department_name ORDER BY e.salary DESC) AS salary_rank,
    AVG(e.salary) OVER (PARTITION BY d.department_name) AS dept_avg_salary
FROM employees e
INNER JOIN departments d ON e.department_id = d.id
WHERE e.status = 'active'
ORDER BY d.department_name, salary_rank;
""",
    """\
INSERT INTO report_summary (report_date, category, total_sales, avg_order_value)
SELECT
    CURRENT_DATE AS report_date,
    c.category_name,
    COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS total_sales,
    COALESCE(AVG(oi.quantity * oi.unit_price), 0) AS avg_order_value
FROM categories c
LEFT JOIN products p ON c.id = p.category_id
LEFT JOIN order_items oi ON p.id = oi.product_id
LEFT JOIN orders o ON oi.order_id = o.id AND o.order_date = CURRENT_DATE
GROUP BY c.category_name
ON CONFLICT (report_date, category)
DO UPDATE SET
    total_sales = EXCLUDED.total_sales,
    avg_order_value = EXCLUDED.avg_order_value;
""",
]

PYTHON_SNIPPETS = [
    """\
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://localhost:5432/analytics")

query = \"\"\"
    SELECT date, product_id, SUM(revenue) as total_revenue
    FROM sales
    WHERE date >= '2025-01-01'
    GROUP BY date, product_id
\"\"\"

df = pd.read_sql(query, engine)
df['rolling_avg'] = df.groupby('product_id')['total_revenue'].transform(
    lambda x: x.rolling(window=7, min_periods=1).mean()
)

pivot = df.pivot_table(
    values='total_revenue',
    index='date',
    columns='product_id',
    aggfunc='sum',
    fill_value=0
)
print(pivot.tail(10))
""",
    """\
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


@dataclass
class Transaction:
    id: int
    amount: float
    currency: str
    timestamp: datetime
    status: str = "pending"
    metadata: dict = field(default_factory=dict)

    @property
    def is_completed(self) -> bool:
        return self.status == "completed"

    def approve(self) -> None:
        if self.status != "pending":
            raise ValueError(f"Cannot approve transaction in {self.status} state")
        self.status = "completed"
        self.metadata["approved_at"] = datetime.now().isoformat()


def process_batch(transactions: list[Transaction]) -> dict:
    results = {"approved": 0, "failed": 0, "total_amount": 0.0}
    for txn in transactions:
        try:
            txn.approve()
            results["approved"] += 1
            results["total_amount"] += txn.amount
        except ValueError:
            results["failed"] += 1
    return results
""",
    """\
import asyncio
import aiohttp
from typing import Any


async def fetch_data(session: aiohttp.ClientSession, url: str) -> dict[str, Any]:
    async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
        response.raise_for_status()
        return await response.json()


async def fetch_all_pages(base_url: str, max_pages: int = 10) -> list[dict]:
    results = []
    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_data(session, f"{base_url}?page={page}")
            for page in range(1, max_pages + 1)
        ]
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        for resp in responses:
            if isinstance(resp, dict):
                results.extend(resp.get("data", []))
    return results


async def main():
    data = await fetch_all_pages("https://api.example.com/records")
    print(f"Fetched {len(data)} records")


if __name__ == "__main__":
    asyncio.run(main())
""",
    """\
from collections import defaultdict
from functools import lru_cache


def analyze_log_file(filepath: str) -> dict:
    error_counts = defaultdict(int)
    endpoint_latencies = defaultdict(list)

    with open(filepath, "r") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) < 4:
                continue

            timestamp, level, endpoint, latency_ms = parts[:4]

            if level.strip() == "ERROR":
                error_counts[endpoint.strip()] += 1

            endpoint_latencies[endpoint.strip()].append(float(latency_ms))

    summary = {}
    for endpoint, latencies in endpoint_latencies.items():
        summary[endpoint] = {
            "avg_latency": sum(latencies) / len(latencies),
            "max_latency": max(latencies),
            "p95_latency": sorted(latencies)[int(len(latencies) * 0.95)],
            "error_count": error_counts.get(endpoint, 0),
            "request_count": len(latencies),
        }
    return summary
""",
    """\
import sqlite3
from contextlib import contextmanager


@contextmanager
def get_db_connection(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def migrate_schema(db_path: str) -> None:
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(\"\"\"
            CREATE TABLE IF NOT EXISTS migrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        \"\"\")
        cursor.execute(\"\"\"
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        \"\"\")
        print("Schema migration completed successfully")
""",
]

ALL_SNIPPETS = SQL_SNIPPETS + PYTHON_SNIPPETS


def get_random_snippet() -> str:
    """Return a random code snippet from the collection."""
    return random.choice(ALL_SNIPPETS)
