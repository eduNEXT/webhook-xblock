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


@shared_task(
    bind=True,
    autoretry_for=(Timeout),
    retry_backoff=True,
    retry_kwargs={
        "max_retries": MAX_RETRIES,
    },
)
def task_send_payload(self, data, url):  # pylint: disable=unused-argument
    """
    Task that Triggers the webhook and sends the payload
    """
    course_id = data.get("course_id")

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
