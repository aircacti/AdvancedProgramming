import sys
import time

import pika

RABBIT_HOST = "localhost"
RABBIT_PORT = 8081
PASSES = "guest"
QUEUE_NAME = "jobs"
JOB_DURATION = 10


def connect():
    parameters = pika.ConnectionParameters(
        host=RABBIT_HOST,
        port=RABBIT_PORT,
        credentials=pika.PlainCredentials(PASSES, PASSES),
    )
    return pika.BlockingConnection(parameters)


def do_job(channel, method, properties, body) -> None:
    job_id = body.decode()

    print(f"Wykonuje {job_id}")
    time.sleep(JOB_DURATION)

    channel.basic_ack(delivery_tag=method.delivery_tag)
    print(f"Zakonczona {job_id}")


if __name__ == "__main__":
    try:
        connection = connect()
    except pika.exceptions.AMQPConnectionError:
        print("Blad laczenia")
        sys.exit(1)

    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=do_job)

    print("Czekam na zadania, Ctrl+C konczy prace")

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
        connection.close()
        print("Koniec")
