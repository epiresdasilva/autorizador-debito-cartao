import json
import logging


def main(event, context):
    print(str(event))

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    body = {
        "mensagem": "Lançamento incluida com sucesso"
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
