# Generated by Django 4.2.3 on 2023-07-23 15:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api01", "0002_transcript_reply"),
    ]

    operations = [
        migrations.AddField(
            model_name="session",
            name="agent",
            field=models.CharField(default="", max_length=500),
        ),
        migrations.AddField(
            model_name="session",
            name="ip",
            field=models.CharField(default="", max_length=20),
        ),
        migrations.AddField(
            model_name="session",
            name="referer",
            field=models.CharField(default="", max_length=500),
        ),
    ]
