from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=80)
    url = models.URLField(max_length=200, blank=True, null=True)
    creator = models.ForeignKey("Coder", on_delete=models.CASCADE, related_name='creator')