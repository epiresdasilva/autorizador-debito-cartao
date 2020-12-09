import boto3
import logging
import os
import uuid
from datetime import datetime


def main(event, context):
    body = event["detail"]

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table_name = os.environ['LANCAMENTO_TABLE']

    table = dynamodb.Table(table_name)

    return table.put_item(
        Item={
            'id': str(uuid.uuid4()),
            'agencia': body["agencia"],
            'numeroConta': body["numeroConta"],
            'numeroCartao': body["numeroCartao"],
            'valor': body["valor"],
            'data': datetime.today().strftime('%Y-%m-%d')
        }
    )
