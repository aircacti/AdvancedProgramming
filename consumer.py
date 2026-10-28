import os
import time

QUEUE_FILE = "queue.txt"
LOCK_FILE = "lock.txt"


def lock() -> None:
    while True:
        try:
            os.mkdir(LOCK_FILE)
            return
        except Exception:
            time.sleep(0.1)


def unlock() -> None:
    os.rmdir(LOCK_FILE)


def read_jobs() -> list:
    jobs = []
    if not os.path.exists(QUEUE_FILE):
        return jobs

    with open(QUEUE_FILE) as f:
        for line in f.read().splitlines():
            job_id, status = line.split(",")
            jobs.append({"id": job_id, "status": status})

    return jobs


def write_jobs(jobs: list) -> None:
    with open(QUEUE_FILE, "w") as f:
        for job in jobs:
            f.write(job["id"] + "," + job["status"] + "\n")


def take_job() -> int:
    lock()
    jobs = read_jobs()
    took_id = None

    for job in jobs:
        if job["status"] == "pending":
            job["status"] = "in_progress"
            took_id = job["id"]
            break

    write_jobs(jobs)
    unlock()
    return took_id


def finish_job(job_id: int) -> None:
    lock()
    jobs = read_jobs()

    for job in jobs:
        if job["id"] == job_id:
            job["status"] = "done"

    write_jobs(jobs)
    unlock()


if __name__ == "__main__":
    while True:
        job_id = take_job()

        if job_id is None:
            time.sleep(5)
        else:
            print(f"Wykonuje {job_id}")
            time.sleep(10)  # Zmieniono z 30 na 10 w pórównaniu z Notion
            finish_job(job_id)
            print(f"Zakończona {job_id}")
