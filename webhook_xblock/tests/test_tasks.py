from unittest import TestCase
from unittest.mock import Mock, patch

from webhook_xblock.tasks import retry_task, task_send_payload


class TestTasks(TestCase):
    """Unit tests for the async tasks."""

    @patch("webhook_xblock.tasks.requests.post")
    def test_task_send_payload_success(self, mock_post):
        """Test that task_send_payload returns True on successful request."""
        mock_post.return_value.ok = True
        data = {"course_id": "course-v1:edX+DemoX+2025_T1"}
        result = task_send_payload(data, "http://example.com")

        self.assertTrue(result)

    @patch("webhook_xblock.tasks.requests.post")
    @patch("webhook_xblock.tasks.retry_task")
    def test_task_send_payload_failure(self, mock_retry_task, mock_post):
        """Test that task_send_payload retries on failure."""
        mock_post.side_effect = Exception("Error")
        data = {"course_id": "course-v1:edX+DemoX+2025_T1"}

        task_send_payload(data, "http://example.com")

        mock_retry_task.assert_called_once()

    @patch("webhook_xblock.tasks.requests.post")
    @patch("webhook_xblock.tasks.LOGGER")
    def test_task_send_payload_response_not_ok(self, mock_logger, mock_post):
        """Test that task_send_payload logs an error and returns False when the response is not OK."""
        mock_post.return_value.ok = False
        mock_post.return_value.status_code = 500
        mock_post.return_value.text = "Internal Server Error"
        data = {"course_id": "course-v1:edX+DemoX+2025_T1"}
        url = "http://example.com/webhook"

        result = task_send_payload(data, url)

        mock_logger.error.assert_called_once_with(
            "Webhook-Xblock request FAILED for course course-v1:edX+DemoX+2025_T1. "
            "status 500 - Internal Server Error"
        )
        self.assertFalse(result)


class TestRetryTask(TestCase):
    """Unit tests for the retry_task function."""

    @patch("webhook_xblock.tasks.LOGGER")
    def test_retry_task_max_retries_exceeded(self, mock_logger):
        """Test that retry_task logs an error and returns False when max retries are exceeded."""

        task = Mock()
        task.request.retries = 3
        task.max_retries = 3
        url = "http://example.com/webhook"
        exception = Exception("Network error")

        result = retry_task(task, exception, url)

        mock_logger.error.assert_called_once_with(
            "Could not send payload to {url}. MAX RETRIES EXCEEDED".format(url=url)
        )
        self.assertFalse(result)

    @patch("webhook_xblock.tasks.LOGGER")
    def test_retry_task_with_custom_countdown(self, mock_logger):
        """Test that retry_task raises a retry exception with the correct countdown."""

        task = Mock()
        task.request.retries = 1
        task.max_retries = 3
        task.retry = Mock(side_effect=Exception("Retrying"))
        url = "http://example.com/webhook"
        exception = Exception("Temporary failure")

        with patch("webhook_xblock.tasks.RETRY_DELAY", 10):
            with self.assertRaises(Exception) as context:
                retry_task(task, exception, url)

            task.retry.assert_called_once_with(exc=exception, countdown=10)
            self.assertEqual(str(context.exception), "Retrying")

        mock_logger.error.assert_not_called()
