import logging
import random
from datetime import datetime

from airflow.decorators import task
from airflow.models import DAG

logging.basicConfig(level=logging.INFO)

with DAG(
    dag_id="simple",
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:

    @task
    def random_number():
        value = random.randint(1, 250)  # Did this jump scare anyone?
        logging.info(f"Random number: {value}")
        return value

    @task(task_id="log_something")
    def log_something(message, number):
        for i in range(number):
            logging.info(f"{i}: {message}")

    # This removes the >> operator portion of the code and makes it more readable.
    number = random_number()
    log_something("Hello, Airflow!", number)
