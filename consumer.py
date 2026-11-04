import os
import sqlite3
import time

CON = sqlite3.connect("identifier.sqlite", timeout=30)
CUR = CON.cursor()
LOCK_FILE = "lock.txt"


def lock() -> None:
    while True:
        try:
            os.mkdir(LOCK_FILE)
            return
        except Exception:
            time.sleep(0.05)


def unlock() -> None:
    try:
        os.rmdir(LOCK_FILE)
    except Exception:
        pass


CUR.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        status TEXT
    )
""")


def take_job():
    lock()
    try:
        row = CUR.execute(
            "SELECT id FROM jobs WHERE status = 'pending' LIMIT 1"
        ).fetchone()

        if not row:
            return None

        job_id = row[0]

        CUR.execute(
            "UPDATE jobs SET status = 'in_progress' WHERE id = ?", (job_id,)
        )
        CON.commit()

        return job_id
    finally:
        unlock()


def finish_job(job_id: int) -> None:
    lock()
    try:
        CUR.execute("UPDATE jobs SET status = 'done' WHERE id = ?", (job_id,))
        CON.commit()
    finally:
        unlock()


if __name__ == "__main__":
    while True:
        job_id = take_job()

        if job_id is None:
            time.sleep(1)
        else:
            print(f"Wykonuje {job_id}")
            time.sleep(10)
            finish_job(job_id)
            print(f"Zakonczona {job_id}")
