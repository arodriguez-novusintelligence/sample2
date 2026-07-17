import json
import os
from decimal import Decimal

import boto3


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            if obj % 1 == 0:
                return int(obj)
            return float(obj)
        return super().default(obj)


def _response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body, cls=DecimalEncoder),
    }


def handler(event, context):
    table_name = os.environ.get("TABLE_NAME")
    if not table_name:
        return _response(200, {"items": [], "count": 0})

    table = boto3.resource("dynamodb").Table(table_name)
    response = table.scan(Limit=50)
    items = response.get("Items", [])
    return _response(200, {"items": items, "count": len(items)})
