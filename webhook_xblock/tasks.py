"""
Async tasks to send the payload.
"""
import requests
from celery import shared_task  # pylint: disable=import-error
from celery.utils.log import get_task_logger  # pylint: disable=import-error

from webhook_xblock.constants import REQUEST_TIMEOUT, RETRY_DELAY

LOGGER = get_task_logger(__name__)

MAX_RETRIES = 3


@shared_task(bind=True, max_retries=MAX_RETRIES)
def task_send_payload(self, data, url):  # pylint: disable=unused-argument,inconsistent-return-statements
    """
    Task that Triggers the webhook and sends the payload
    """
    course_id = data.get("course_id")

    try:
        response = requests.post(
            url=url,
            data=data,
            timeout=REQUEST_TIMEOUT,
        )

        if response.ok:
            return True

        LOGGER.error(
            "Webhook-Xblock request FAILED for course %s. status %s - %s",
            course_id,
            response.status_code,
            getattr(response, "text", ""),
        )
        return False
    except Exception as exc:  # pylint: disable=broad-except
        retry_task(self, exc, url)


def retry_task(task, exception, url):
    """
    Calls the task to run again in case it has not exceeded the
    number of max_retries.
    """
    if task.request.retries >= task.max_retries:
        LOGGER.error("Could not send payload to %s. MAX RETRIES EXCEEDED", url)
        return False

    raise task.retry(exc=exception, countdown=RETRY_DELAY)
