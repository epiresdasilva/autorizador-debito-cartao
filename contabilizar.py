import boto3
import logging
import os
import uuid


def main(event, context):
    body = event["detail"]

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table_name = os.environ['CONTABILIZACAO_TABLE']

    table = dynamodb.Table(table_name)

    return table.put_item(
        Item={
            'id': str(uuid.uuid4()),
            'registros': [
                {
                    "contaContabil": "1.0.0.0.01",
                    "valor": body["valor"],
                    "documento": body["numeroCartao"],
                    "natureza": "CREDITO"
                },
                {
                    "contaContabil": "2.0.0.0.01",
                    "valor": body["valor"],
                    "documento": body["numeroCartao"],
                    "natureza": "DEBITO"
                }
            ]
        }
    )
