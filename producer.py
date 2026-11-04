import sqlite3

CON = sqlite3.connect("identifier.sqlite", timeout=30)
CUR = CON.cursor()

CUR.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        status TEXT
    )
""")

CUR.execute("INSERT INTO jobs (status) VALUES (?)", ("pending",))
CON.commit()

new_job_id = CUR.lastrowid
print(f"Dodano {new_job_id},pending")

CON.close()
