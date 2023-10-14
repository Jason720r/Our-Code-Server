from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    date = models.DateField()
    poster = models.ForeignKey("Coder", on_delete=models.CASCADE, related_name='poster')
    likers = models.ManyToManyField("Coder", related_name="coder_liked")