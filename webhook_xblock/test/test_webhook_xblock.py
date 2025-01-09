from django.test import TestCase
from webhook_xblock.webhook_xblock import WebhookXblock


class WebhookXblockBasicTests(TestCase):
    """
    Basic test to validate that WebhookXblock initializes correctly.
    """

    def test_xblock_initialization(self):
        """
        Verifies that a WebhookXblock instance initializes with default values.
        """
        xblock = WebhookXblock()
        self.assertIsNotNone(xblock)
