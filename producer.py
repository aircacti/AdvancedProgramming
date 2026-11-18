import sys
import uuid

import pika

RABBIT_HOST = "localhost"
RABBIT_PORT = 8081
PASSES = "guest"
QUEUE_NAME = "jobs"


def connect():
    parameters = pika.ConnectionParameters(
        host=RABBIT_HOST,
        port=RABBIT_PORT,
        credentials=pika.PlainCredentials(PASSES, PASSES),
    )
    return pika.BlockingConnection(parameters)


def add_job(channel) -> str:
    job_id = str(uuid.uuid4())

    channel.basic_publish(
        exchange="",
        routing_key=QUEUE_NAME,
        body=job_id,
        properties=pika.BasicProperties(delivery_mode=2),
    )

    return job_id


if __name__ == "__main__":
    try:
        connection = connect()
    except pika.exceptions.AMQPConnectionError:
        print("Blad laczenia")
        sys.exit(1)

    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    new_job_id = add_job(channel)
    print(f"Dodano {new_job_id},pending")

    connection.close()
