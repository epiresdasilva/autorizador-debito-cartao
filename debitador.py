import json
import logging
import psycopg2
import rds_config


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
                        returning saldo;
                        """)
        result = cursor.fetchone()
        saldo = float(result[0])

        if saldo < 0:
            connection.rollback()
        else:
            connection.commit()
    except psycopg2.Error as e:
        connection.rollback()
        logger.error("Error while inserting", e)

    status_code = 200
    body = {
        "saldo": saldo
    }

    if saldo < 0:
        status_code = 409
        body = {
            "mensagem": "Saldo insuficiente"
        }

    response = {
        "statusCode": status_code,
        "body": json.dumps(body)
    }

    return response
