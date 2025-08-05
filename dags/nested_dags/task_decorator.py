import logging
from datetime import datetime

from airflow.decorators import task
from airflow.models import DAG
from utils.addition import add as add_util
from utils.subtraction import subtract as subtract_util

with DAG(
    dag_id="taskflow_api_example",
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:

    @task(task_id="add_task")
    def add_task(a, b):
        return add_util(a, b)

    @task(task_id="subtract_task")
    def subtract_task(a, b):
        return subtract_util(a, b)

    @task(task_id="result_task")
    def result_task(result):
        logging.info(f"Result: {result}")

    # Example 1:
    # Use a and b to calculate a final value of 8

    a = 5
    b = 7

    sum1 = add_task(a, a)
    sum2 = add_task(sum1, a)
    final_value = subtract_task(sum2, b)
    result_task(final_value)
