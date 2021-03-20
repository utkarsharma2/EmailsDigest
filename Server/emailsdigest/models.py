from django.db import models

class Application(models.Model):
    """Class to keep configs of application"""

    name = models.CharField(max_length=255, unique=True, null=False, blank=False)
    duration = models.IntegerField(default=60, blank=False, null=False)
    distribution_list = models.CharField(max_length=5000, null=False, blank=False)
    forward_unique = models.BooleanField(default=True, null=False, blank=False)
    threshold = models.FloatField(default=0.1, null=False, blank=False)

    def __str__(self):
        return self.name

class Email(models.Model):
    """Class to maintain email data"""

    subject = models.TextField(default="")
    body = models.TextField(default="")
    label = models.UUIDField(null=False)
    app = models.ForeignKey(Application, null=False, on_delete=models.CASCADE, blank=False)
    is_sent = models.BooleanField(default=False, blank=False, null=False)
    is_leader = models.BooleanField(default=False, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, blank=False, null=False)

    def __str__(self):
        return f'{str(self.label)} -- {self.created} -- {self.subject}'
