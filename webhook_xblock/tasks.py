"""
Async tasks to send the payload.
"""
import requests
from celery import shared_task  # pylint: disable=import-error
from celery.utils.log import get_task_logger  # pylint: disable=import-error
from requests.exceptions import Timeout

from webhook_xblock.constants import REQUEST_TIMEOUT

LOGGER = get_task_logger(__name__)

MAX_RETRIES = 3


@shared_task(bind=True, max_retries=MAX_RETRIES)
def task_send_payload(self, data, url):  # pylint: disable=unused-argument
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
        else:
            LOGGER.error("Webhook-Xblock request FAILED for course {course}. status {code} - {msg}".format(
                code=response.status_code,
                msg=getattr(response, "text", ""),
                course=course_id,
            ))
            return False
    except Exception as exc:  # pylint: disable=broad-except
        retry_task(self, exc, url)


def retry_task(task, exception, url):
    """
    Calls the task to run again in case it has not exceeded the
    number of max_retries.
    """
    if task.request.retries >= task.max_retries:
        LOGGER.error("Could not send payload to {url}. MAX RETRIES EXCEEDED".format(
            url=url
        ))
        return False

    raise task.retry(exc=exception, countdown=RETRY_DELAY)

