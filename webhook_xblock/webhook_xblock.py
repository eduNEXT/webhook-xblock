"""
This XBlock was created to send basic information about the course and
student to a configurable URL, when visiting a specific course unit.
"""
# pylint: disable=import-error

import datetime
import json
import logging

import pkg_resources
import requests
from django.contrib.auth import get_user_model
from django.utils import translation
from opaque_keys.edx.keys import CourseKey
from xblock.core import XBlock
from xblock.fields import Boolean, Dict, Scope, String
from xblock.fragment import Fragment
from xblockutils.resources import ResourceLoader

from webhook_xblock.constants import REQUEST_TIMEOUT
from webhook_xblock.edxapp_wrapper.grade import get_student_course_grade
from webhook_xblock.edxapp_wrapper.user import get_serialized_user_account
from webhook_xblock.tasks import task_send_payload
from webhook_xblock.utils import flatten_dict

LOGGER = logging.getLogger(__name__)


class WebhookXblock(XBlock):  # pylint: disable=too-many-instance-attributes
    """
    XBlock that triggers a specific webhook, it sends
    a payload with basic information about the course and
    student to a configurable URL.
    """

    checkpoint = Boolean(
        default=False,
        scope=Scope.user_state,
        help="Indicates if the student has already visited this course unit",
    )
    name = String(
        default=None,
        scope=Scope.content,
        help="String to identify the triggered course component that sends the payload",
    )
    webhook_url = String(
        default=None,
        scope=Scope.content,
        help="URL of the webhook to send the payload to",
    )
    extra_info = Dict(
        default={},
        scope=Scope.content,
        help="Extra information to send in the payload",
    )
    send_course_grade = Boolean(
        default=False,
        scope=Scope.content,
        help="Indicates if the course grade should be sent in the payload",
    )
    send_async = Boolean(
        default=False,
        scope=Scope.content,
        help="Indicates if the payload should be sent in an async task",
    )
    frequency = String(
        default="one-time",
        scope=Scope.content,
        help="How often should the payload be sent",
    )
    button_text = String(
        default="send payload",
        scope=Scope.content,
        help="Button inner HTML",
    )
    component_text = String(
        default="",
        scope=Scope.content,
        help="Extra text to show in the component",
    )

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def check_if_running_from_studio(self):
        """
        Helper that returns True if the XBlock is currently
        being called from studio mode, otherwise returns False.
        """
        is_studio = hasattr(self.xmodule_runtime, "is_author_mode")  # pylint: disable=no-member
        if (
            is_studio
            or self.xmodule_runtime.__class__.__name__ == "StudioEditModuleRuntime"  # pylint: disable=no-member
        ):
            return True

        return False

    def make_request(self, data):
        """
        Helper for sending the request to the payload.
        """
        response = requests.post(self.webhook_url, data, timeout=REQUEST_TIMEOUT)
        if not response.ok:
            LOGGER.error(
                "Webhook-Xblock request FAILED for course %s. status %s - %s",
                response.status_code,
                getattr(response, "text", ""),
                data['course_id'],
            )

        return response.ok

    def mark_as_visited(self):
        """
        Helper called when the student visits the course unit with the
        webhook component.
        Returns True only when the frequency is "one-time",
        and the unit has not been visited yet, otherwise
        returns False.
        """
        if self.frequency == 'one-time' and not self.checkpoint:
            self.checkpoint = True
            return True

        return False

    def get_course_grade(self, course_id, username):
        """
        Returns a dict containing the student's course grade.
        In case an exception is raised, returns an empty dictionary.

        In case there is no exception raised, the fields
        in the response dictionary are:
            * passed: Boolean representing whether the course has been
                    passed according to the course's grading policy.
            * percent: A float representing the overall grade for the course
            * letter_grade: A letter grade as defined in grading policy
                    (e.g. 'A' 'B' 'C') or None
        """
        grade = {}

        try:
            grade_user = get_user_model().objects.get(username=username)
            course_key = CourseKey.from_string(course_id)
            course_grade = get_student_course_grade(grade_user, course_key=course_key)

            grade = {
                'passed': course_grade.passed,
                'percent': course_grade.percent,
                'letter_grade': course_grade.letter_grade,
            }
        # We make this a broad except to catch any exception.
        except Exception as err:  # pylint: disable=broad-except
            LOGGER.error(
                'Could not retrieve grades for %s user in course %s: %s',
                username,
                course_id,
                err,
            )

        return grade

    def student_view(self, context=None):  # pylint: disable=unused-argument
        """
        The primary view of the WebhookXblock, shown to students
        when viewing courses.
        """
        html = self.resource_string("static/html/webhook_xblock.html")
        frag = Fragment(html.format(
            self=self,
            frequency=self.frequency,
            button_text=self.button_text,
            component_text=self.component_text,
            studio_mode=self.check_if_running_from_studio(),
        ))
        frag.add_css(self.resource_string("static/css/webhook_xblock.css"))

        # Add i18n js
        statici18n_js_url = self._get_statici18n_js_url()
        if statici18n_js_url:
            frag.add_javascript_url(self.runtime.local_resource_url(self, statici18n_js_url))

        frag.add_javascript(self.resource_string("static/js/src/webhook_xblock.js"))
        frag.initialize_js('WebhookXblock')
        return frag

    def studio_view(self, context=None):  # pylint: disable=unused-argument
        """
        Creates a fragment used to display the edit view in the Studio.
        This view allows the user (staff) to set the webhook configurations.
        """
        html = self.resource_string("static/html/webhook_xblock_edit.html")
        frag = Fragment(html.format(
            self=self,
            frequency=self.frequency,
            extra_info=json.dumps(self.extra_info).replace("\"", "&quot;"),
            send_course_grade=self.send_course_grade,
            send_async=self.send_async,
            component_text=self.component_text,
            button_text=self.button_text,
            webhook_url=self.webhook_url or "",
            name=self.name or "",
        ))
        frag.add_css(self.resource_string("static/css/webhook_xblock.css"))

        frag.add_javascript(self.resource_string("static/js/src/webhook_xblock_edit.js"))
        frag.initialize_js('WebhookXblockEditBlock')
        return frag

    @XBlock.json_handler
    def send_payload(self, data, suffix=''):  # pylint: disable=unused-argument
        """
        Handler that triggers the webhook and sends the payload.
        """
        if not self.check_if_running_from_studio() and (self.frequency != 'one-time' or self.mark_as_visited()):
            current_anonymous_student_id = self.runtime.anonymous_student_id
            course_id = str(self.runtime.course_id)
            student = self.runtime.get_real_user(current_anonymous_student_id)
            serialized_student = get_serialized_user_account(student)
            response = False

            payload = {
                "payload_name": self.name,
                "timestamp": datetime.datetime.now().isoformat(),
                "anonymous_student_id": current_anonymous_student_id,
                "student": serialized_student.data,
                "course_id": course_id,
            }
            payload.update(self.extra_info)

            # Check if we have to send the course grade for the student
            if self.send_course_grade:
                payload.update(self.get_course_grade(course_id, student.username))

            payload = flatten_dict(payload)

            if self.send_async:
                task_result = task_send_payload.delay(payload, self.webhook_url)
                if task_result.ready():
                    response = task_result.result
            else:
                response = self.make_request(payload)

            return {"sent_payload": response}

        return {}

    @XBlock.json_handler
    def studio_submit(self, data, suffix=''):  # pylint: disable=unused-argument
        """
        Called when submitting the form in Studio.
        Saves all the XBlock fields values entered by the user (staff).
        """
        extra_info_err = 'The extra information could not be saved. Field has an incorrect format'

        self.webhook_url = data.get('webhook_url')
        self.name = data.get('name')
        self.frequency = data.get('frequency')
        self.send_course_grade = data.get('send_course_grade')
        self.send_async = data.get('send_async')
        self.component_text = data.get('component_text')
        if self.frequency == 'sent-by-student':
            self.button_text = data.get('button_text')

        try:
            self.extra_info = json.loads(data.get('extra_info', {}))
        except ValueError:
            LOGGER.error(extra_info_err)
        else:
            if not isinstance(self.extra_info, dict):
                self.extra_info = {}
                LOGGER.error(extra_info_err)

        return {'result': 'success'}

    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("WebhookXblock",
             """<webhook-xblock/>
             """),
            ("Multiple WebhookXblock",
             """<vertical_demo>
                <webhook-xblock/>
                <webhook-xblock/>
                <webhook-xblock/>
                </vertical_demo>
             """),
        ]

    @staticmethod
    def _get_statici18n_js_url():
        """
        Returns the Javascript translation file for the currently
        selected language, if any. Defaults to English if available.
        """
        locale_code = translation.get_language()
        if locale_code is None:
            return None
        text_js = 'public/js/translations/{locale_code}/text.js'
        lang_code = locale_code.split('-')[0]
        for code in (locale_code, lang_code, 'en'):
            loader = ResourceLoader(__name__)
            if pkg_resources.resource_exists(
                    loader.module_name, text_js.format(locale_code=code)):
                return text_js.format(locale_code=code)
        return None

    @staticmethod
    def get_dummy():
        """
        Dummy method to generate initial i18n
        """
        return translation.gettext_noop('Dummy')
