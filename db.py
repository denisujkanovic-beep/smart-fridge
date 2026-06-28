import sqlite3

def get_conn():
    return sqlite3.connect("fridge.db", check_same_thread=False)


def init():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS fridge (
        item TEXT PRIMARY KEY,
        amount INTEGER
    )
    """)

    # default data jen pokud je prázdno
    c.execute("SELECT COUNT(*) FROM fridge")
    if c.fetchone()[0] == 0:
        c.executemany("INSERT INTO fridge VALUES (?, ?)", [
            ("mléko", 2),
            ("máslo", 1),
            ("vejce", 6),
            ("šunka", 0),
            ("sýr", 0)
        ])

    conn.commit()
    conn.close()
