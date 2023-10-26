from celery import shared_task, Task

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from accounts.models import CustomUser
from .utils import send_email


class BaseTaskWithRetry(Task):
    autoretry_for = (Exception,)
    retry_kwargs = {'max_retries': 5}
    retry_backoff = True
    retry_jitter = False
    task_acks_late = True
    worker_concurrency = 4
    worker_prefetch_multiplier = 1
    task_time_limit = 120


@shared_task(base=BaseTaskWithRetry)
def send_confirmation(user_id, order_status="Processing"):
    user = CustomUser.objects.get(id=user_id)
    email_body = email_message(user, order_status)
    email_data = {"email_body": email_body, "to_email": user.email, "email_subject": "Reset The Password"}
    send_email(email_data)


def email_message(user, order_status):
    message = {
        "Processing": f"Hello {user.username},\n your order has been submitted and is processing",
        "Shipping": f"Hello {user.username},\n your order has been shipped",
        "Delivered": f"Hello {user.username},\n your order has been delivered",
        "Returned": f"Hello {user.username},\n your order has been returned"
    }
    return message[order_status]
