import json
import logging
import psycopg2
import rds_config
import boto3


def main(event, context):
    body = json.loads(event["body"])

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # rds settings
    rds_host = rds_config.db_host
    name = rds_config.db_username
    password = rds_config.db_password
    db_name = rds_config.db_name

    connection = psycopg2.connect(
        database=db_name,
        user=name,
        password=password,
        host=rds_host,
        port='5432'
    )
    cursor = connection.cursor()

    try:
        cursor.execute(f"""
                        update conta_corrente set saldo = saldo - {body["valor"]}
                        where numero_cartao = {body["numeroCartao"]}
                        returning saldo, agencia, numero_conta;
                        """)
        result = cursor.fetchone()
        saldo = float(result[0])
        agencia = result[1]
        numero_conta = result[2]

        if saldo < 0:
            connection.rollback()
        else:
            connection.commit()
    except psycopg2.Error as e:
        connection.rollback()
        logger.error("Error while inserting", e)

    conta = {
        "agencia": agencia,
        "numeroConta": numero_conta,
        "numeroCartao": body["numeroCartao"],
        "valor": body["valor"]
    }

    if saldo < 0:
        return error_response(conta)

    return success_response(conta)


def success_response(body):
    status_code = 200

    client = boto3.client('events')

    bridge_response = client.put_events(
        Entries=[
            {
                'Source': 'debitador',
                'DetailType': 'debitador',
                'Detail': json.dumps(body)
            },
        ]
    )
    print(str(bridge_response))

    return {
        "statusCode": status_code,
        "body": json.dumps(body)
    }


def error_response(body):
    status_code = 409
    body["mensagem"] = "Saldo insuficiente"

    return {
        "statusCode": status_code,
        "body": json.dumps(body)
    }

