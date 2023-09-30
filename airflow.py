from airflow import DAG
from airflow.operators.python import PythonOperator
from process_files import process_files
from process_file import process_file
from list_files_to_queue import list_files
import datetime
import get_config

default_args = {
    'owner': 'Optimus Prime Transformers',
    'start_date': datetime(2023, 9, 11),
    'retries': 1,
}

# Define the DAG
dag = DAG(
    'opt_processing_dag',
    default_args=default_args,
    schedule_interval=None, 
    catchup=False,
    max_active_runs=1,
)

config = get_config
files = list_files(config.get('data_dir'))
    
for file in files:
        try: 
            process_task = PythonOperator(task_id=f'{file}', 
                                          python_callable=process_file,
                                          op_kwargs={'filename':file, 'config':config})
        except Exception as e: 
            print(f"Error: {e}")
        
        