# Use the official Airflow image as a base
FROM apache/airflow:2.9.2

# Install jq
USER root
RUN apt-get update && apt-get install -y jq

# Switch back to airflow user
USER airflow
