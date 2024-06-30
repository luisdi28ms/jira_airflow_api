# Manage JIRA's Alerts with Airflow
A small project showcasing my knowledge of integrating API's and Airflow workflows.

## Check Airflow Alert dag

The [Check Airflow alert dag](/dags/check_airflow_alert.py) runs daily and leverages [JIRA Service Management ops REST API](https://developer.atlassian.com/cloud/jira/service-desk-ops/rest/v2/api-group-alerts/#api-group-alerts) to automate the following steps:

1. Generate an alert with a given message.

2. Get the latest alert ID.

3. Check if the flow is running on a weekday or weekend:
    * If running on a weekday add a note to the alert.
    * If running on a weekend add another note to the alert.

![dag graph](/img/check_airflow_alert_graph.jpeg)

## Check Airflow Alert results

![dag result](/img/check_airflow_aler_result.jpeg)

# Run App

## Requirements

A JIRA account with a JIRA Service Management Project.
* JIRA User email
* JIRA Cloud ID
* JIRA API Key

## Getting Started

1. Get docker image.
```sh
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.9.2/docker-compose.yaml'
```
Note: To install extra packages, create Dockerfile with 
packages and point to it in the docker-compose. In this example, jq was installed to
enable extracting key details from a task and input them into the next one.

2. Initialize environment.
```sh
mkdir -p ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

3. Build the image.
```sh
docker compose build
``` 

4. Initialize the databse.
```sh
docker compose up airflow-init
```
The account created has the login airflow and the password airflow.

5. Start all services.

```sh
docker compose up
```

6. To run airflow commands.

```sh
% curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.9.2/airflow.sh'
chmod +x airflow.sh
```

```sh
./airflow.sh bash
```

7. Add the JIRA variables.

* JIRA_CLOUD_ID
* JIRA_EMAIL
* JIRA_API_KEY

```sh
airflow variables set <key> <value>
```