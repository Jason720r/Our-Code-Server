from django.db import models

class Event(models.Model):
    name = models.CharField(max_length=40)
    organizer = models.ForeignKey("Coder", on_delete=models.CASCADE, related_name='organizer')
    number_of_people = models.IntegerField()
    attendees = models.ManyToManyField("Coder", related_name="attended_events")
    description = models.CharField(max_length=150)
    location = models.CharField(max_length=200)
    type = models.ForeignKey("Category", on_delete=models.CASCADE, related_name='type')
    date = models.DateField()