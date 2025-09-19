import sqlite3

# Connect (creates items.db if not exists)
conn = sqlite3.connect("items.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    price REAL
)
""")

# Insert fruits and vegetables (price per kg in ₹)
items = [
    ("apple", 120),
    ("banana", 60),
    ("orange", 100),
    ("mango", 150),
    ("grapes", 120),
    ("tomato", 40),
    ("Potato", 30),
    ("onion", 35),
    ("carrot", 50),
    ("cucumber", 45),
    ("spinach", 25),
    ("Cauliflower", 55),
    ("Cabbage", 40),
    ("Green Beans", 70),
    ("Papaya", 80),
]

cursor.executemany("INSERT OR IGNORE INTO products (name, price) VALUES (?, ?)", items)

# Save & close
conn.commit()
conn.close() 

print("✅ items.db created with fruits and vegetables!")
