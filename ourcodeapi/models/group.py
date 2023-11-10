from django.db import models

class Group(models.Model):
    name = models.CharField(max_length=50)
    creator = models.ForeignKey("Coder", on_delete=models.CASCADE, related_name='group_creator')
    moderator = models.ManyToManyField("Coder", related_name="moderator")
    group_user = models.ManyToManyField("Coder", related_name="group_user")
    description = models.CharField(max_length=120)
