import json
import os
import sys
import unittest
from decimal import Decimal
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import calculator


def _event(method, path, body=None):
    event = {"routeKey": f"{method} {path}"}
    if body is not None:
        event["body"] = json.dumps(body)
    return event


class CalculatorHandlerTests(unittest.TestCase):
    def setUp(self):
        os.environ.pop("TABLE_NAME", None)

    @patch("calculator.boto3")
    def test_add_persists_when_table_configured(self, mock_boto3):
        os.environ["TABLE_NAME"] = "sample2-calculations-dev"
        mock_table = MagicMock()
        mock_boto3.resource.return_value.Table.return_value = mock_table

        response = calculator.handler(
            _event("POST", "/calculate", {"operation": "add", "left": 2, "right": 3}),
            None,
        )

        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(json.loads(response["body"]), {"result": 5})
        mock_table.put_item.assert_called_once()
        item = mock_table.put_item.call_args.kwargs["Item"]
        self.assertEqual(item["operation"], "add")
        self.assertEqual(item["left"], Decimal("2"))
        self.assertEqual(item["right"], Decimal("3"))
        self.assertEqual(item["result"], Decimal("5"))

    def test_subtract_without_table(self):
        response = calculator.handler(
            _event("POST", "/calculate", {"operation": "subtract", "left": 10, "right": 4}),
            None,
        )

        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(json.loads(response["body"]), {"result": 6})

    def test_multiply(self):
        response = calculator.handler(
            _event("POST", "/calculate", {"operation": "multiply", "left": 3, "right": 7}),
            None,
        )

        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(json.loads(response["body"]), {"result": 21})

    def test_divide(self):
        response = calculator.handler(
            _event("POST", "/calculate", {"operation": "divide", "left": 8, "right": 2}),
            None,
        )

        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(json.loads(response["body"]), {"result": 4})

    def test_divide_by_zero_returns_400(self):
        response = calculator.handler(
            _event("POST", "/calculate", {"operation": "divide", "left": 1, "right": 0}),
            None,
        )

        self.assertEqual(response["statusCode"], 400)
        self.assertEqual(json.loads(response["body"]), {"error": "Division by zero"})

    def test_invalid_operation_returns_400(self):
        response = calculator.handler(
            _event("POST", "/calculate", {"operation": "power", "left": 2, "right": 3}),
            None,
        )

        self.assertEqual(response["statusCode"], 400)
        self.assertEqual(json.loads(response["body"]), {"error": "Invalid operation"})

    def test_invalid_operands_returns_400(self):
        response = calculator.handler(
            _event("POST", "/calculate", {"operation": "add", "left": "x", "right": 1}),
            None,
        )

        self.assertEqual(response["statusCode"], 400)
        self.assertEqual(json.loads(response["body"]), {"error": "Invalid operands"})

    def test_invalid_json_returns_400(self):
        response = calculator.handler(
            {"routeKey": "POST /calculate", "body": "{not-json"},
            None,
        )

        self.assertEqual(response["statusCode"], 400)
        self.assertEqual(json.loads(response["body"]), {"error": "Invalid JSON body"})

    def test_health_returns_ok(self):
        response = calculator.handler(_event("GET", "/health"), None)

        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(
            json.loads(response["body"]),
            {"status": "ok", "service": "sample2-calculator"},
        )


if __name__ == "__main__":
    unittest.main()
