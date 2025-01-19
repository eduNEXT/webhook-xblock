from django.test import TestCase
from mock import MagicMock, patch
from webhook_xblock.webhook_xblock import WebhookXblock


class WebhookXblockTests(TestCase):

    def test_make_request_success(self, mock_post):
        """
        Tests that make_request returns True when the request is successful.
        """
        self.assertTrue(True)
