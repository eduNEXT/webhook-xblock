"""
Production settings for the Webhook-xblock plugin.
"""


def plugin_settings(settings):
    """
    Read / Update necessary project settings for production envs.
    """
    settings.WEBHOOK_USER_MODULE_BACKEND = getattr(settings, "ENV_TOKENS", {}).get(
        "WEBHOOK_USER_MODULE_BACKEND",
        settings.WEBHOOK_USER_MODULE_BACKEND
    )
    settings.WEBHOOK_GRADE_MODULE_BACKEND = getattr(settings, "ENV_TOKENS", {}).get(
        "WEBHOOK_GRADE_MODULE_BACKEND",
        settings.WEBHOOK_GRADE_MODULE_BACKEND
    )
