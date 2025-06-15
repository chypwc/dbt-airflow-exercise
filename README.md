# ELT Pipeline with Apache Airflow and dbt

This project demonstrates a complete **Extract-Load-Transform (ELT)** data pipeline using **Apache Airflow**, **Docker**, and **dbt**. It loads data from a source PostgreSQL database, transforms it with `dbt`, and stores results in a destination PostgreSQL database.

## 🛠️ Project Components

- **Apache Airflow**: Workflow orchestrator to manage ELT steps.
- **dbt (Data Build Tool)**: SQL-based transformations on the destination database.
- **PostgreSQL (source & destination)**: Simulated databases for data movement.
- **Docker Compose**: For containerized and reproducible development setup.

## 📂 Directory Structure

```
.
├── airflow/
│   └── dags/
│       └── elt_dag.py               # Contains main DAG and trigger DAG
├── customer_postgres/              # dbt project directory
├── elt_script/
│   └── elt_script.py               # Python script for data extraction and loading
├── source_db_init/
│   └── init.sql                    # Sample data for the source database
├── Dockerfile                      # Custom Airflow image with providers installed
├── docker-compose.yml              # Services configuration
└── README.md
```

## 🚀 Pipeline Overview

1. **Trigger DAG** (`trigger_elt_once`)

   - Runs once on startup and triggers the main ELT workflow.

2. **Main DAG** (`elt_and_dbt`)
   - **`run_elt_script`**: PythonOperator that extracts data from source PostgreSQL and loads it into destination PostgreSQL.
   - **`dbt_run`**: DockerOperator that runs `dbt run` inside a container to transform the data.

## 🐳 Getting Started

1. Start the Project

```bash
docker compose up --build
```

2. Access Airflow UI
   • URL: http://localhost:8080
   • Login: airflow
   • Password: airflow

## 📚 References

This project learns from the GitHub repository: justinbchau/custom-elt-project
# dbt-airflow-exercise
