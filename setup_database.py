
import csv
import sqlite3
from pathlib import Path

# ------------------------------------------
# PATHS
# ------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
DATABASE_DIR = BASE_DIR / "database"

DATABASE_DIR.mkdir(exist_ok=True)

DB_PATH = DATABASE_DIR / "smartration_large.db"

CSV_PATH = (
    DATA_DIR /
    "SmartRation_expanded_registered_beneficiaries.csv"
)

# ------------------------------------------
# CHECK CSV
# ------------------------------------------

if not CSV_PATH.exists():
    raise FileNotFoundError(
        f"CSV file not found: {CSV_PATH}"
    )

# ------------------------------------------
# PROTECT EXISTING DATABASE
# ------------------------------------------

if DB_PATH.exists():
    conn = sqlite3.connect(DB_PATH)

    existing = conn.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name='beneficiaries'
    """).fetchone()

    if existing:
        conn.close()
        raise RuntimeError(
            "Beneficiary database already exists. "
            "Nothing was changed. Do not run setup again."
        )
else:
    conn = sqlite3.connect(DB_PATH)

# ------------------------------------------
# CREATE TABLE
# ------------------------------------------

conn.execute("""
CREATE TABLE beneficiaries (
    beneficiary_id TEXT PRIMARY KEY,
    name TEXT,
    bpl_number TEXT,
    family_members INTEGER,
    district TEXT,
    taluk TEXT,
    hobli TEXT,
    village TEXT,
    ration_shop TEXT,
    token TEXT,
    queue_status TEXT,
    synthetic_record TEXT,
    category TEXT,
    verification_status TEXT
)
""")

# ------------------------------------------
# IMPORT CSV
# ------------------------------------------

columns = [
    "beneficiary_id",
    "name",
    "bpl_number",
    "family_members",
    "district",
    "taluk",
    "hobli",
    "village",
    "ration_shop",
    "token",
    "queue_status",
    "synthetic_record",
    "category",
    "verification_status"
]

batch = []
imported = 0
batch_size = 5000

try:

    with open(
        CSV_PATH,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        missing = [
            col for col in columns
            if col not in (reader.fieldnames or [])
        ]

        if missing:
            raise ValueError(
                "Missing CSV columns: " + ", ".join(missing)
            )

        sql = """
        INSERT INTO beneficiaries (
            beneficiary_id, name, bpl_number,
            family_members, district, taluk, hobli,
            village, ration_shop, token, queue_status,
            synthetic_record, category, verification_status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        for row in reader:

            values = [
                (row.get(col) or "").strip() or None
                for col in columns
            ]

            batch.append(values)

            if len(batch) >= batch_size:
                conn.executemany(sql, batch)
                conn.commit()

                imported += len(batch)
                print(f"Imported {imported:,} records")

                batch.clear()

        if batch:
            conn.executemany(sql, batch)
            conn.commit()
            imported += len(batch)

    # --------------------------------------
    # CREATE INDEXES
    # --------------------------------------

    conn.execute("""
        CREATE INDEX idx_beneficiary_login
        ON beneficiaries(name, bpl_number)
    """)

    conn.execute("""
        CREATE INDEX idx_beneficiary_location
        ON beneficiaries(district, taluk, village)
    """)

    conn.commit()

    total = conn.execute(
        "SELECT COUNT(*) FROM beneficiaries"
    ).fetchone()[0]

    print("\nDATABASE CREATED SUCCESSFULLY!")
    print("Imported records:", imported)
    print("Database records:", total)
    print("Database path:", DB_PATH)

except Exception:
    conn.rollback()
    raise

finally:
    conn.close()
