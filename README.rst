Webhook XBlock
==============

This repository provides an X-block that triggers a webhook by sending a payload with basic information 
about the course and student to a configurable URL.

The XBlock can be set in three modes:
* Send the payload every time the user visits the course unit
* Send the payload only the first time the user visits the course unit (default mode)
* Allow the student to send the request by clicking on a button

Other **available configurations** are:
* Add a text to the component to show to the student
* Configure the button text (in case the student is allowed to send the payload)
* Send extra information in the payload
* Send the student's course grade

Description of the payload
---------------------------

* **payload_name**: A string to help identify the course component that is sending the payload.
* **anonymous_student_id**: A string that contains an anonymized identifier of the student.
* **timestamp**: Timestamp for when the student visits the XBlock component.
* **student_is_active**: Boolean that indicates whether the student is active on the platform.
* **student_email**: Email of the student.
* **student_date_joined**: Timestamp for when the student got registered on the platform.
* **student_username**: Username of the student.

If the *Send course grade* option is enabled, three extra fields are added:
* **passed**: Boolean representing whether the course has been passed according to the course's grading policy.
* **percent**: A float representing the overall grade for the course.
* **letter_grade**: A letter grade as defined in grading policy (e.g., 'A', 'B', 'C') or None.


.. code-block:: JSON
        {
            'payload_name': 'course-started', 
            'anonymous_student_id': '8db9fe4e00b4f713d37187bb363fb7cc', 
            'percent': 0.0, 
            'timestamp': '2021-07-26T07:28:47.243653', 
            'passed': False, 
            'student_is_active': True, 
            'student_email': 'test@example.com', 
            'course_id': 'course-v1:edunext+01+test', 
            'student_date_joined': '2021-04-22T13:15:43.457066-05:00', 
            'student_username': 'testUser', 
            'letter_grade': None
        }


Compatibility Notes
--------------------

+------------------+---------------+
| Open edX Release | Version       |
+==================+===============+
| Ironwood         | < 1.0.0       |
+------------------+---------------+
| Juniper          | < 1.0.0       |
+------------------+---------------+
| Koa              | < 1.0.0       |
+------------------+---------------+
| Lilac            | < 1.0.0       |
+------------------+---------------+
| Maple            | < 1.0.0       |
+------------------+---------------+
| Nutmeg           | < 1.0.0       |
+------------------+---------------+
| Olive            | < 1.0.0       |
+------------------+---------------+
| Palm             | < 1.0.0       |
+------------------+---------------+
| Quince           | < 1.0.0       |
+------------------+---------------+
| Redwood          | >= 1.0.0      |
+------------------+---------------+
| Sumac            | >= 1.0.0      |
+------------------+---------------+

Usage
=======

Enabling XBlock in Studio
------------------

You can enable the Webhook XBlock in Studio by
modifying the advanced settings for your course:

* Navigate to **Settings** -> **Advanced Settings** and go to the **Advanced Module List** setting.
* To enable the XBlock for your course, add `"webhook-xblock"` to the list and save the changes.

Configure XBlock
------------------

First, enable the XBlock in Studio.

Once you add a webhook component to the course, you can
then click on "edit" to make the configurations.


Testing with Docker
====================

This XBlock comes with a Docker test environment ready to build, based on the xblock-sdk workbench. To build and run it::

    $ make dev.run

The XBlock SDK Workbench, including this XBlock, will be available on the list of XBlocks at http://localhost:8000

Translating
=============

Internationalization (i18n) is when a program is made aware of multiple languages.
Localization (l10n) is adapting a program to local language and cultural habits.

Use the locale directory to provide internationalized strings for your XBlock project.
For more information on how to enable translations, visit the
`Open edX XBlock tutorial on Internationalization <https://edx.readthedocs.org/projects/xblock-tutorial/en/latest/edx_platform/edx_lms.html>`_.

This cookiecutter template uses `django-statici18n <https://django-statici18n.readthedocs.io/en/latest/>`_
to provide translations to static javascript using ``gettext``.

The included Makefile contains targets for extracting, compiling and validating translatable strings.
The general steps to provide multilingual messages for a Python program (or an XBlock) are:

1. Mark translatable strings.
2. Run i18n tools to create raw message catalogs.
3. Create language specific translations for each message in the catalogs.
4. Use ``gettext`` to translate strings.

1. Mark translatable strings
-----------------------------

Mark translatable strings in python::


    from django.utils.translation import ugettext as _

    # Translators: This comment will appear in the `.po` file.
    message = _("This will be marked.")

See `edx-developer-guide <https://edx.readthedocs.io/projects/edx-developer-guide/en/latest/internationalization/i18n.html#python-source-code>`_
for more information.

You can also use ``gettext`` to mark strings in javascript::


    // Translators: This comment will appear in the `.po` file.
    var message = gettext("Custom message.");

See `edx-developer-guide <https://edx.readthedocs.io/projects/edx-developer-guide/en/latest/internationalization/i18n.html#javascript-files>`_
for more information.

2. Run i18n tools to create Raw message catalogs
-------------------------------------------------

This cookiecutter template offers multiple make targets which are shortcuts to
use `edx-i18n-tools <https://github.com/edx/i18n-tools>`_.

After marking strings as translatable we have to create the raw message catalogs.
These catalogs are created in ``.po`` files. For more information see
`GNU PO file documentation <https://www.gnu.org/software/gettext/manual/html_node/PO-Files.html>`_.
These catalogs can be created by running::


    $ make extract_translations

The previous command will create the necessary ``.po`` files under
``webhook-xblock/webhook_xblock/locale/en/LC_MESSAGES/text.po``.
The ``text.po`` file is created from the ``django-partial.po`` file created by
``django-admin makemessages`` (`makemessages documentation <https://docs.djangoproject.com/en/2.2/topics/i18n/translation/#message-files>`_),
this is why you will not see a ``django-partial.po`` file.

3. Create language specific translations
----------------------------------------------

3.1 Add translated strings
***************************

After creating the raw message catalogs, all translations should be filled out by the translator.
One or more translators must edit the entries created in the message catalog, i.e. the ``.po`` file(s).
The format of each entry is as follows::

    #  translator-comments
    A. extracted-comments
    #: reference…
    #, flag…
    #| msgid previous-untranslated-string
    msgid 'untranslated message'
    msgstr 'mensaje traducido (translated message)'

For more information see
`GNU PO file documentation <https://www.gnu.org/software/gettext/manual/html_node/PO-Files.html>`_.

To use translations from transifex use the follow Make target to pull translations::

    $ make pull_translations

See `config instructions <https://github.com/edx/i18n-tools#transifex-commands>`_ for information on how to set up your
transifex credentials.

See `transifex documentation <https://docs.transifex.com/integrations/django>`_ for more details about integrating
django with transiflex.

3.2 Compile translations
*************************

Once translations are in place, use the following Make target to compile the translation catalogs ``.po`` into
``.mo`` message files::

    $ make compile_translations

The previous command will compile ``.po`` files using
``django-admin compilemessages`` (`compilemessages documentation <https://docs.djangoproject.com/en/2.2/topics/i18n/translation/#compiling-message-files>`_).
After compiling the ``.po`` file(s), ``django-statici18n`` is used to create language specific catalogs. See
``django-statici18n`` `documentation <https://django-statici18n.readthedocs.io/en/latest/>`_ for more information.

To upload translations to transiflex use the follow Make target::

    $ make push_translations

See `config instructions <https://github.com/edx/i18n-tools#transifex-commands>`_ for information on how to set up your
transifex credentials.

See `transifex documentation <https://docs.transifex.com/integrations/django>`_ for more details about integrating
django with transiflex.

 **Note:** The ``dev.run`` make target will automatically compile any translations.

 **Note:** To check if the source translation files (``.po``) are up-to-date run::

     $ make detect_changed_source_translations

4. Use ``gettext`` to translate strings
----------------------------------------

Django will automatically use ``gettext`` and the compiled translations to translate strings.

Troubleshooting
================

If there are any errors compiling ``.po`` files run the following command to validate your ``.po`` files::

    $ make validate

See `django's i18n troubleshooting documentation
<https://docs.djangoproject.com/en/2.2/topics/i18n/translation/#troubleshooting-gettext-incorrectly-detects-python-format-in-strings-with-percent-signs>`_
for more information.
