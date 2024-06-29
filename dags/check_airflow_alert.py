from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import BranchPythonOperator
from airflow.models import Variable
from datetime import datetime
import pendulum

JIRA_CLOUD_ID = Variable.get("JIRA_CLOUD_ID")
JIRA_API_KEY = Variable.get("JIRA_API_KEY")
JIRA_EMAIL = Variable.get("JIRA_EMAIL")


create_alert_cmd = '''
curl --request POST \
  --url "https://api.atlassian.com/jsm/ops/api/{{ var.value.JIRA_CLOUD_ID }}/v1/alerts" \
  --user "{{ var.value.JIRA_EMAIL }}:{{ var.value.JIRA_API_KEY }}" \
  --header "Accept: application/json" \
  --header "Content-Type: application/json" \
  --data '{"message":"Please check Airflow!"}'
'''

get_latest_alert_id_cmd = '''
response=$(curl --silent --request GET \
  --url "https://api.atlassian.com/jsm/ops/api/{{ var.value.JIRA_CLOUD_ID }}/v1/alerts" \
  --user "{{ var.value.JIRA_EMAIL }}:{{ var.value.JIRA_API_KEY }}" \
  --header 'Accept: application/json')

first_alert_id=$(echo "$response" | jq -r '.values[0].id')

echo "$first_alert_id"
'''

add_weekday_note_cmd = '''
curl --request POST \
  --url "https://api.atlassian.com/jsm/ops/api/{{ var.value.JIRA_CLOUD_ID }}/v1/alerts/{{ task_instance.xcom_pull(task_ids='get_latest_alert_id') }}/notes" \
  --user "{{ var.value.JIRA_EMAIL }}:{{ var.value.JIRA_API_KEY }}" \
  --header "Accept: application/json" \
  --header "Content-Type: application/json" \
  --data '{"note": "It iss time to work."}'
'''

add_weekend_note_cmd = '''
curl --request POST \
  --url "https://api.atlassian.com/jsm/ops/api/{{ var.value.JIRA_CLOUD_ID }}/v1/alerts/{{ task_instance.xcom_pull(task_ids='get_latest_alert_id') }}/notes" \
  --user "{{ var.value.JIRA_EMAIL }}:{{ var.value.JIRA_API_KEY }}" \
  --header "Accept: application/json" \
  --header "Content-Type: application/json" \
  --data '{"note": "Do not worry, it can wait until Monday."}'
'''

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 6, 26),
    'schedule_interval': None,
}

def choose_branch():
    today = pendulum.now().day_of_week
    if today < 5:  # Monday is 0 and Sunday is 6
        return 'add_weekday_note'
    else:
        return 'add_weekend_note'

with DAG('check_airflow_alert', default_args=default_args) as dag:
    t1 = BashOperator(
        task_id='create_alert',
        bash_command=create_alert_cmd
    )

    t2 = BashOperator(
        task_id='get_latest_alert_id',
        bash_command=get_latest_alert_id_cmd,
        do_xcom_push=True
    )

    t3 = BranchPythonOperator(
        task_id='check_weekday_or_weekend',
        python_callable=choose_branch,
    )

    t4 = BashOperator(
        task_id='add_weekday_note',
        bash_command=add_weekday_note_cmd
    )

    t5 = BashOperator(
        task_id='add_weekend_note',
        bash_command=add_weekend_note_cmd
    )

    t1 >> t2 >> t3
    t3 >> [t4, t5]
