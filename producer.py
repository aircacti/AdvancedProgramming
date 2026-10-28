import os

QUEUE_FILE = "queue.txt"

job_id = 0
if os.path.exists(QUEUE_FILE):
    with open(QUEUE_FILE) as f:
        job_id = len(f.readlines())

new_job_id = job_id + 1

with open(QUEUE_FILE, 'a') as f:
    f.write(f"{new_job_id},pending\n")

print(f"Dodano: {new_job_id},pending")
