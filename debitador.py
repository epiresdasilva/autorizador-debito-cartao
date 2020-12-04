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
                        where numero_cartao = {body["numero_cartao"]}
                        returning saldo;
                        """)
        result = cursor.fetchone()

        connection.commit()
    except psycopg2.Error as e:
        connection.rollback()
        logger.error("Error while inserting", e)

    body = {
        "saldo": float(result[0])
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

