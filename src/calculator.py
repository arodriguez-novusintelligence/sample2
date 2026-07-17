import json
import os
import uuid
from decimal import Decimal

import boto3

OPERATIONS = {
    "add": lambda left, right: left + right,
    "subtract": lambda left, right: left - right,
    "multiply": lambda left, right: left * right,
    "divide": lambda left, right: left / right,
}


def _response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }


def _parse_body(event):
    raw_body = event.get("body")
    if raw_body is None:
        return {}

    if event.get("isBase64Encoded"):
        import base64

        raw_body = base64.b64decode(raw_body).decode("utf-8")

    try:
        return json.loads(raw_body)
    except (json.JSONDecodeError, TypeError):
        return None


def _to_number(value):
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return value
    if isinstance(value, str):
        try:
            if "." in value:
                return float(value)
            return int(value)
        except ValueError:
            return None
    return None


def _to_decimal(value):
    if isinstance(value, float):
        return Decimal(str(value))
    return Decimal(value)


def _persist(table_name, operation, left, right, result):
    table = boto3.resource("dynamodb").Table(table_name)
    table.put_item(
        Item={
            "id": str(uuid.uuid4()),
            "operation": operation,
            "left": _to_decimal(left),
            "right": _to_decimal(right),
            "result": _to_decimal(result),
        }
    )


def calculate(event):
    payload = _parse_body(event)
    if payload is None:
        return _response(400, {"error": "Invalid JSON body"})

    operation = payload.get("operation")
    left = _to_number(payload.get("left"))
    right = _to_number(payload.get("right"))

    if operation not in OPERATIONS:
        return _response(400, {"error": "Invalid operation"})
    if left is None or right is None:
        return _response(400, {"error": "Invalid operands"})
    if operation == "divide" and right == 0:
        return _response(400, {"error": "Division by zero"})

    result = OPERATIONS[operation](left, right)

    table_name = os.environ.get("TABLE_NAME")
    if table_name:
        _persist(table_name, operation, left, right, result)

    return _response(200, {"result": result})


def health(event):
    return _response(200, {"status": "ok", "service": "sample2-calculator"})


def handler(event, context):
    route_key = event.get("routeKey")
    if not route_key:
        request_context = event.get("requestContext", {})
        http = request_context.get("http", {})
        method = http.get("method") or event.get("httpMethod")
        path = event.get("rawPath") or event.get("path", "")
        route_key = f"{method} {path}"

    if route_key == "GET /health":
        return health(event)
    if route_key == "POST /calculate":
        return calculate(event)

    return _response(404, {"error": "Not found"})
