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
        cursor.execute("""
                        CREATE TABLE IF NOT EXISTS conta_corrente (
                            id serial PRIMARY KEY,
                            agencia integer,
                            numero_conta integer,
                            saldo numeric(15,2),
                            numero_cartao bigint
                        );
                        """)

        cursor.execute(f"""
                        insert into conta_corrente(agencia, numero_conta, saldo, numero_cartao)
                        values ({body["agencia"]}, {body["numeroConta"]}, {body["saldo"]}, {body["numeroCartao"]});
                        """)

        connection.commit()
    except psycopg2.Error as e:
        connection.rollback()
        logger.error("Error while inserting", e)

    body = {
        "mensagem": "Conta incluida com sucesso"
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
