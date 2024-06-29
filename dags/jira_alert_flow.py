from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.models import Variable
from datetime import datetime

JIRA_CLOUD_ID = Variable.get("JIRA_CLOUD_ID")
JIRA_API_KEY = Variable.get("JIRA_API_KEY")

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 6, 26),
    'schedule_interval': None,
}

list_alerts_cmd = f'''
curl --request GET \
  --url "https://api.atlassian.com/jsm/ops/api/{JIRA_CLOUD_ID}/v1/alerts" \
  --user "luisdi28ms@gmail.com:{JIRA_API_KEY}" \
  --header 'Accept: application/json'
'''

create_alert_cmd = f'''
curl --request POST \
  --url "https://api.atlassian.com/jsm/ops/api/{JIRA_CLOUD_ID}/v1/alerts" \
  --user "luisdi28ms@gmail.com:{JIRA_API_KEY}" \
  --header "Accept: application/json" \
  --header "Content-Type: application/json" \
  --data '{{"message":"Airflow ran fine!"}}'
'''

with DAG('jira_alert_flow', default_args=default_args) as dag:
    t1 = BashOperator(
        task_id='list_alerts',
        bash_command=list_alerts_cmd
    )

    t2 = BashOperator(
        task_id='create_alert',
        bash_command=create_alert_cmd
    )

    t1 >> t2