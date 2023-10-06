from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from list_files_to_queue import list_files_to_queue
from process_files_from_queue import process_files_from_queue

default_args = {
    'owner': 'transformers',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(seconds=5),
}

dag = DAG(
    'my_dag',
    default_args=default_args,
    description='Orchestration of list_files_to_queue and process_files_from_queue',
    schedule_interval=None,  # Set to None to manually trigger the DAG
    catchup=False,
    max_active_runs=1,
    dagrun_timeout=timedelta(hours=2),
    tags=['my_dag'],
)

def calculate_execution_time(**kwargs):
    # Calculate execution times based on execution_date
    task1_start_time = kwargs['execution_date'] + timedelta(seconds=0)
    task2_start_time = kwargs['execution_date'] + timedelta(seconds=15)
    return task1_start_time, task2_start_time

task1_start_time, task2_start_time = PythonOperator(
    task_id='calculate_execution_time',
    python_callable=calculate_execution_time,
    provide_context=True,
    dag=dag,
)

list_files_task = PythonOperator(
    task_id='list_files_task',
    python_callable=list_files_to_queue,
    provide_context=True,
    dag=dag,
    execution_date="{{ task_instance.xcom_pull(task_ids='calculate_execution_time')[0] }}"
)

process_files_task = PythonOperator(
    task_id='process_files_task',
    python_callable=process_files_from_queue,
    provide_context=True,
    dag=dag,
    execution_date="{{ task_instance.xcom_pull(task_ids='calculate_execution_time')[1] }}"
)

# Set task dependencies
task1_start_time >> list_files_task
task1_start_time >> process_files_task

if __name__ == "__main__":
    dag.cli()
