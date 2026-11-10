
import sqlite3

db_path = "database/smartration_large.db"

conn = sqlite3.connect(db_path)

tables = conn.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
""").fetchall()

print("\nDATABASE TABLES:")
for table in tables:
    print("-", table[0])

if any(table[0] == "beneficiaries" for table in tables):

    count = conn.execute("""
        SELECT COUNT(*)
        FROM beneficiaries
    """).fetchone()[0]

    print("\nTOTAL BENEFICIARIES:", count)

    columns = conn.execute("""
        PRAGMA table_info(beneficiaries)
    """).fetchall()

    print("\nBENEFICIARY COLUMNS:")
    for column in columns:
        print("-", column[1])

else:
    print("\nBeneficiaries table not found.")

conn.close()
