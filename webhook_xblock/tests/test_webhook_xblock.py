from django.test import TestCase
from mock import MagicMock, patch
from webhook_xblock.webhook_xblock import WebhookXblock


class WebhookXblockTests(TestCase):

    def setUp(self):
        """
        Initial setup for the tests.
        """
        self.xblock = WebhookXblock()
        self.xblock.webhook_url = "http://example.com/webhook"
        self.xblock.name = "test_component"
        self.xblock.frequency = "one-time"

    @patch("webhook_xblock.webhook_xblock.requests.post")
    def test_make_request_success(self, mock_post):
        """
        Tests that make_request returns True when the request is successful.
        """
        mock_response = MagicMock()
        mock_response.ok = True
        mock_post.return_value = mock_response

        data = {"test_key": "test_value"}
        result = self.xblock.make_request(data)
        self.assertTrue(result)

    @patch("webhook_xblock.webhook_xblock.requests.post")
    def test_make_request_failure(self, mock_post):
        """
        Tests that make_request returns False when the request fails.
        """
        mock_response = MagicMock()
        mock_response.ok = False
        mock_post.return_value = mock_response

        data = {"test_key": "test_value"}
        result = self.xblock.make_request(data)
        self.assertFalse(result)

    @patch("webhook_xblock.webhook_xblock.requests.post", side_effect=Exception("Test exception"))
    def test_make_request_exception(self, mock_post):
        """
        Tests that make_request handles exceptions correctly.
        """
        data = {"test_key": "test_value"}
        with self.assertRaises(Exception):
            self.xblock.make_request(data)

    def test_mark_as_visited_first_time(self):
        """
        Tests that mark_as_visited returns False if it has already been visited.
        """
        self.xblock.checkpoint = False
        result = self.xblock.mark_as_visited()
        self.assertTrue(result)

    def test_mark_as_visited_already_visited(self):
        """
        Prueba que mark_as_visited retorna False si ya ha sido visitado.
        """
        self.xblock.checkpoint = True
        result = self.xblock.mark_as_visited()
        self.assertFalse(result)

    def test_flatten_dict_integration(self):
        """
        Tests the integration of flatten_dict with the XBlock.
        """
        input_dict = {"a": {"b": {"c": 1}}, "d": 2}
        expected = {"a_b_c": 1, "d": 2}
        result = self.xblock.flatten_dict(input_dict)
        self.assertEqual(result, expected)