"""Unit tests for the WebhookXblock class."""
import datetime
import json
from unittest import TestCase
from unittest.mock import Mock, patch

from webhook_xblock.webhook_xblock import REQUEST_TIMEOUT, WebhookXblock


def mock_json_handler(func):
    """Mock decorator to replace @XBlock.json_handler."""
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


class TestWebhookXblock(TestCase):
    """Unit tests for the WebhookXblock class."""

    def setUp(self):
        """Set up common test attributes."""
        self.runtime = Mock()
        self.runtime.course_id = "course-v1:edX+DemoX+2025_T1"
        self.runtime.anonymous_student_id = "student123"
        self.xblock = WebhookXblock(runtime=self.runtime, scope_ids=Mock())
        self.xblock.webhook_url = "http://example.com/webhook"
        self.xblock.name = "Test Webhook"
        self.xblock.extra_info = {"key": "value"}
        self.xblock.send_course_grade = True
        self.xblock.send_async = False
        self.xblock.frequency = "one-time"
        self.xblock.checkpoint = False

    @patch("webhook_xblock.webhook_xblock.requests.post")
    def test_make_request_success(self, mock_post):
        """Test that make_request sends a POST request and returns True on success."""
        mock_post.return_value.ok = True
        data = {"key": "value"}

        result = self.xblock.make_request(data)

        mock_post.assert_called_once_with(self.xblock.webhook_url, data, timeout=REQUEST_TIMEOUT)
        self.assertTrue(result)

    @patch("webhook_xblock.webhook_xblock.requests.post")
    def test_make_request_failure(self, mock_post):
        """Test that make_request logs an error and returns False on failure."""
        mock_post.return_value.ok = False
        mock_post.return_value.status_code = 500
        mock_post.return_value.text = "Server Error"
        data = {"course_id": "course-v1:edX+DemoX+2025_T1"}

        result = self.xblock.make_request(data)

        mock_post.assert_called_once_with(self.xblock.webhook_url, data, timeout=REQUEST_TIMEOUT)
        self.assertFalse(result)

    def test_mark_as_visited_one_time_frequency(self):
        """Test that mark_as_visited sets the checkpoint for one-time frequency."""
        result = self.xblock.mark_as_visited()

        self.assertTrue(result)
        self.assertTrue(self.xblock.checkpoint)

    def test_mark_as_visited_already_visited(self):
        """Test that mark_as_visited returns False if checkpoint is already set."""
        self.xblock.checkpoint = True

        result = self.xblock.mark_as_visited()

        self.assertFalse(result)

    @patch("webhook_xblock.webhook_xblock.User")
    @patch("webhook_xblock.webhook_xblock.CourseGradeFactory")
    def test_get_course_grade_success(self, mock_course_grade_factory, mock_user_model):
        """Test that get_course_grade returns the correct grade information."""
        mock_user = Mock()
        mock_user.username = "student123"
        mock_user_model.objects.get.return_value = mock_user

        mock_course_grade = Mock()
        mock_course_grade.passed = True
        mock_course_grade.percent = 0.85
        mock_course_grade.letter_grade = "B"
        mock_course_grade_factory().read.return_value = mock_course_grade

        grade = self.xblock.get_course_grade("course-v1:edX+DemoX+2025_T1", "student123")

        self.assertEqual(grade, {"passed": True, "percent": 0.85, "letter_grade": "B"})

    @patch("webhook_xblock.webhook_xblock.User")
    def test_get_course_grade_exception(self, mock_user_model):
        """Test that get_course_grade returns an empty dict on exception."""
        mock_user_model.objects.get.side_effect = Exception("Error")

        grade = self.xblock.get_course_grade("course-v1:edX+DemoX+2025_T1", "student123")

        self.assertEqual(grade, {})
