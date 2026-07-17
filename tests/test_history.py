import json
import os
import sys
import unittest
from decimal import Decimal
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import history


class HistoryHandlerTests(unittest.TestCase):
    def setUp(self):
        os.environ.pop("TABLE_NAME", None)

    def test_returns_empty_list_without_table_name(self):
        response = history.handler({"routeKey": "GET /history"}, None)

        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(json.loads(response["body"]), {"items": [], "count": 0})

    @patch("history.boto3")
    def test_returns_scanned_items(self, mock_boto3):
        os.environ["TABLE_NAME"] = "sample2-calculations-dev"
        items = [
            {
                "id": "abc-123",
                "operation": "add",
                "left": Decimal("2"),
                "right": Decimal("3"),
                "result": Decimal("5"),
            }
        ]
        mock_table = MagicMock()
        mock_table.scan.return_value = {"Items": items}
        mock_boto3.resource.return_value.Table.return_value = mock_table

        response = history.handler({"routeKey": "GET /history"}, None)

        self.assertEqual(response["statusCode"], 200)
        body = json.loads(response["body"])
        self.assertEqual(body["count"], 1)
        self.assertEqual(len(body["items"]), 1)
        self.assertEqual(body["items"][0]["operation"], "add")
        mock_table.scan.assert_called_once_with(Limit=50)


if __name__ == "__main__":
    unittest.main()
