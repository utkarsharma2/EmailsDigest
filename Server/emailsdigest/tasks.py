from __future__ import absolute_import, unicode_literals

from celery import shared_task
from celery.decorators import task
from celery.utils.log import get_task_logger

from emailsdigest import controller, models

logger = get_task_logger(__name__)


@task(name="label_emails")
def label_emails(email, app_name):
    app = models.Application.objects.filter(name=app_name).first()
    label, is_leader = controller.label_email(email, app)
    email_obj = models.Email()
    email_obj.body = email['body']
    email_obj.subject = email['subject']
    email_obj.label = label
    email_obj.is_leader = is_leader
    email_obj.app = app
    email_obj.save()

    if app.forward_unique and is_leader:
        controller.send_email(
            email_obj.subject,
            email_obj.body,
            [app.distribution_list]
        )