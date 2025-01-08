"""
Test Django settings for webhook_xblock project.
"""
from __future__ import unicode_literals

import codecs
import os

import yaml


class SettingsClass:
    """ dummy settings class """


SETTINGS = SettingsClass()
vars().update(SETTINGS.__dict__)
INSTALLED_APPS = vars().get("INSTALLED_APPS", [])
TEST_INSTALLED_APPS = [
    "django.contrib.sites",
]
for app in TEST_INSTALLED_APPS:
    if app not in INSTALLED_APPS:
        INSTALLED_APPS.append(app)

# For testing
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    },
}


def plugin_settings(settings):  # pylint: disable=function-redefined
    """
    Set of plugin settings used by the Open Edx platform.
    More info: https://github.com/openedx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
    """
    settings.EOX_TAGGING_SKIP_VALIDATIONS = True
    settings.EOX_TAGGING_LOAD_PERMISSIONS = False
    settings.DATA_API_DEF_PAGE_SIZE = 1000
    settings.DATA_API_MAX_PAGE_SIZE = 5000
    settings.TEST_SITE = 1

    # setup the databases used in the tutor local environment
    lms_cfg = os.environ.get('LMS_CFG')
    if lms_cfg:
        with codecs.open(lms_cfg, encoding='utf-8') as file:
            env_tokens = yaml.safe_load(file)
        settings.DATABASES = env_tokens['DATABASES']


SETTINGS = SettingsClass()
plugin_settings(SETTINGS)
vars().update(SETTINGS.__dict__)
