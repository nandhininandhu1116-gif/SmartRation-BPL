import sqlite3

DB_PATH = "database/smartration_large.db"

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

checks = {
    "BENEFICIARY SAMPLE": """
        SELECT beneficiary_id, name, bpl_number, district,
               taluk, hobli, village, ration_shop, mobile
        FROM beneficiaries LIMIT 3
    """,
    "USER ACCOUNT SAMPLE": """
        SELECT id, username, beneficiary_id,
               requested_category, priority_status
        FROM user_accounts LIMIT 3
    """,
    "QUEUE SAMPLE": """
        SELECT beneficiary_id, token, category, status,
               priority_verified, district, taluk, village
        FROM queue_records LIMIT 3
    """,
    "STOCK SAMPLE": """
        SELECT district, taluk, village, rice, ragi, wheat
        FROM village_stock LIMIT 5
    """
}

for title, query in checks.items():
    print("\n" + "=" * 55)
    print(title)
    print("=" * 55)

    for row in cur.execute(query):
        print(dict(row))

conn.close()