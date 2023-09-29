import json
import requests

from chalice import Chalice

app = Chalice(app_name="notes_metrics")


import boto3
import os
from botocore.exceptions import ClientError


def get_secret():

    secret_name = "notes-metrics"
    region_name = "us-east-1"

    if os.environ['STAGE'] != "prod":
        session = boto3.session.Session(aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
                                        aws_secret_access_key=os.environ['AWS_SECRET'])
    else:
        session = boto3.session.Session()
        
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    secret_dict = json.loads(get_secret_value_response['SecretString'])
    return secret_dict[secret_name]


@app.route('/')
def index():
    token = get_secret()
    url = "https://api.github.com/repos/qthurier/notes/stats/participation"
    headers = {'Accept': 'application/vnd.github+json',
               'Authorization': f'Bearer {token}',
               'X-GitHub-Api-Version': '2022-11-28'}
    r = requests.get(url=url, headers=headers)
    data = r.json()
    activity_variation = data["owner"][-1] - data["owner"][-2]
    activity_relative_variation = abs(activity_variation/data["owner"][-2])

    if activity_variation >= 0:
        return f"Your activity has increased by {activity_relative_variation:0.0%} compared to last week."
    else:
        return f"Your activity has decreased by {activity_relative_variation:0.0%} compared to last week."