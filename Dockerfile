# Install required providers
FROM apache/airflow:2.8.1

# USER root

# Install providers using airflow user and --user flag
RUN pip install --user --no-cache-dir \
    'apache-airflow[postgres,password]' \
    apache-airflow-providers-docker

# USER airflow