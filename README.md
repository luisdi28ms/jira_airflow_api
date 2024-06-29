# jira_airflow_api
A small project showcasing my knowledge of integrating API's and Airflow workflows.

1. Get docker image.
```sh
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.9.2/docker-compose.yaml'
```
Note: Change demo examples to false.

2. Initialize environment.
```sh
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

3. Initialize the databse.
```sh
docker compose up airflow-init
```
The account created has the login airflow and the password airflow.

4. Start all services.

```sh
docker compose up
```

5. 

```sh
jira_airflow_api % curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.9.2/airflow.sh'
chmod +x airflow.sh
```

```sh
jira_airflow_api % ./airflow.sh bash
```
