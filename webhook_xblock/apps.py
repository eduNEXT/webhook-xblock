"""
WebhookXblock Django application initialization.
"""

from django.apps import AppConfig


class WebhookXblockConfig(AppConfig):
    """
    Configuration for the WebhookXblock Django application.
    """
    name = "webhook_xblock"

    plugin_app = {
        "settings_config": {
            "lms.djangoapp": {
                "common": {"relative_path": "settings.common"},
                "test": {"relative_path": "settings.test"},
                "production": {"relative_path": "settings.production"},
            },
            "cms.djangoapp": {
                "common": {"relative_path": "settings.common"},
                "test": {"relative_path": "settings.test"},
                "production": {"relative_path": "settings.production"},
            },
        }
    }
