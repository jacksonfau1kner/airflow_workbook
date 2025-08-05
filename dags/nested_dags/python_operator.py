import logging
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from utils.addition import add as add_util
from utils.subtraction import subtract as subtract_util


def add_task(a, b, **context):
    return add_util(a, b)


def add_task_sum2(b, **context):
    ti = context["ti"]
    sum1_result = ti.xcom_pull(task_ids="sum1")
    return add_util(sum1_result, b)


def subtract_task(b, **context):
    ti = context["ti"]
    sum2_result = ti.xcom_pull(task_ids="sum2")
    return subtract_util(sum2_result, b)


def result_task(**context):
    ti = context["ti"]
    final_result = ti.xcom_pull(task_ids="final_value")
    logging.info(f"Result: {final_result}")


default_args = {
    "start_date": datetime(2024, 1, 1),
}

with DAG(
    dag_id="python_operator_example",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
) as dag:
    a = 5
    b = 7

    sum1 = PythonOperator(
        task_id="sum1",
        python_callable=add_task,
        op_kwargs={"a": a, "b": a},
    )

    sum2 = PythonOperator(
        task_id="sum2",
        python_callable=add_task_sum2,
        op_kwargs={"b": a},
    )

    final_value = PythonOperator(
        task_id="final_value",
        python_callable=subtract_task,
        op_kwargs={"b": b},
    )

    result = PythonOperator(
        task_id="result",
        python_callable=result_task,
    )

    sum1 >> sum2 >> final_value >> result
