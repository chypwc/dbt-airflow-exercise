from datetime import datetime, timedelta
from airflow import DAG
from docker.types import Mount
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
import subprocess

# --------------------------
# Main DAG: elt_and_dbt
# --------------------------

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
}

def run_elt_script():
    script_path = "/opt/airflow/elt_script/elt_script.py"
    result = subprocess.run(["python", script_path],
                            capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Script failed with error: {result.stderr}")
    else:
        print(result.stdout)


dag_elt_and_dbt = DAG(
    'elt_and_dbt',
    default_args=default_args,
    description='An ELT workflow with dbt',
    start_date=datetime(2025, 6, 16),
    schedule_interval=None,  # Don't auto-trigger, we will trigger manually
    catchup=False,
)

t1 = PythonOperator(
    task_id='run_elt_script',
    python_callable=run_elt_script,
    dag=dag_elt_and_dbt,
)

t2 = DockerOperator(
    task_id='dbt_run',
    image='ghcr.io/dbt-labs/dbt-postgres:1.4.7',
    command=[
        "run",
        "--profiles-dir",
        "/root",
        "--project-dir",
        "/dbt",
        "--full-refresh"
    ],
    auto_remove=True,
    docker_url="unix://var/run/docker.sock",
    network_mode="bridge",
    mounts=[
        Mount(source='/Users/cy/Documents/Courses/data_engineering_youtube/elt/customer_postgres',
              target='/dbt', type='bind'),
        Mount(source='/Users/cy/.dbt', target='/root', type='bind'),
    ],
    dag=dag_elt_and_dbt
)

t1 >> t2

# --------------------------
# Bootstrap DAG: trigger_elt_once
# --------------------------
with DAG(
    dag_id='trigger_elt_once',
    start_date=datetime(2025, 6, 15),
    schedule_interval="@once",
    catchup=False,
) as dag_trigger:
    TriggerDagRunOperator(
        task_id="trigger_main_dag",
        trigger_dag_id="elt_and_dbt",
    )