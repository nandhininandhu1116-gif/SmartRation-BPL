
import sqlite3

DB = "database/smartration_large.db"

conn = sqlite3.connect(DB)

tables_to_check = [
    "user_accounts",
    "queue_records",
    "village_stock",
    "distribution_logs",
    "priority_requests",
    "app_queue_records",
    "app_accounts",
    "app_tokens",
    "smart_queue_records"
]

for table in tables_to_check:

    print("\n" + "=" * 50)
    print("TABLE:", table)

    columns = conn.execute(
        f"PRAGMA table_info({table})"
    ).fetchall()

    for column in columns:
        print(column[1], "-", column[2])

    count = conn.execute(
        f"SELECT COUNT(*) FROM [{table}]"
    ).fetchone()[0]

    print("RECORD COUNT:", count)

conn.close()
