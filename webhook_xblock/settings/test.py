"""
Django test settings for webhook_xblock project.
For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
from webhook_xblock.locale.settings import *

SECRET_KEY = "test"

# Plugin settings
WEBHOOK_USER_MODULE_BACKEND = "webhook_xblock.edxapp_wrapper.backends.user_s_test"
WEBHOOK_GRADE_MODULE_BACKEND = "webhook_xblock.edxapp_wrapper.backends.grade_s_test"
