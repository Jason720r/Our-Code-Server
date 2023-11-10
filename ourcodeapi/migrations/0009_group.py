# Generated by Django 4.2.6 on 2023-11-10 21:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ourcodeapi', '0008_event_likers'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=120)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_creator', to='ourcodeapi.coder')),
                ('group_user', models.ManyToManyField(related_name='group_user', to='ourcodeapi.coder')),
                ('moderator', models.ManyToManyField(related_name='moderator', to='ourcodeapi.coder')),
            ],
        ),
    ]