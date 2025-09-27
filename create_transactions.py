import sqlite3

conn = sqlite3.connect("items.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_id TEXT UNIQUE,
    total REAL,
    status TEXT DEFAULT 'PENDING'
)
""")

conn.commit()
conn.close()
print("✅ transactions table created successfully!")