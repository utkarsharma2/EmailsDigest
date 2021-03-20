"""Command module to send labbeled emails"""

import datetime
import smtplib

from Server import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from emailsdigest import controller, models


class Command(BaseCommand):
    """Class to define command"""

    @staticmethod
    def prepare_emails(emails):
        """Prepare emails digest"""

        body = "Grouped email count: " + str(len(emails)) + "\n\n\n"
        for index, email in enumerate(emails):
             body += "=======================Email - " + str(index + 1) + "=========================\n"
             body += "Subject: " + email.subject + " \nBody: " + email.body + "\n\n"
        return body

    def add_arguments(self, parser):
        parser.add_argument('--force',
        help="Force send emails")

    def handle(
        self, *args, **options
    ):  
        """Get labelled emails and send them"""
        print("Step 1 - looking for pending mails.")
        now = timezone.now()
        pending_emails = list(models.Email.objects.filter(is_sent=False, is_leader=True)[:settings.MAX_EMAIL_SEND_LIMIT])
        print(f"step 2 - Got {len(list(pending_emails))} emails.")


        print("step 3 - Preparing grpuping dict")
        # Prepare grouping on - app, label
        grouped_emails = {}
        for email in pending_emails:
            if grouped_emails.get(email.app.name) is None:
                grouped_emails[email.app.name] = {}

            label = str(email.label)

            if grouped_emails[email.app.name].get(label) is None:
                grouped_emails[email.app.name][label] = email

        print("step 4 - Preparing email digest")
        for app_emails in grouped_emails.values():
            for label_email in app_emails.values():
                if label_email.created + datetime.timedelta(
                    minutes=label_email.app.duration) <= now or options['force']:
                    
                    
                    batch_emails = models.Email.objects.filter(
                        app=label_email.app, label=label_email.label)


                    # send emails
                    controller.send_email(
                        batch_emails[0].subject,
                        Command.prepare_emails(batch_emails),
                        [label_email.app.distribution_list]
                    )
                    batch_emails.update(is_sent=True)
                    print("step 5 - Sent")
                else:
                    print("step 5 - Duration not expired")
