from django.db import models

# Create your models here.


class Session(models.Model):
    session_id = models.CharField(max_length=50)
    ip = models.CharField(max_length=20, default="")
    agent = models.CharField(max_length=500, default="")
    referer = models.CharField(max_length=500, default="")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}:{}".format(str(self.session_id), str(self.created))


class Transcript(models.Model):
    session = models.ForeignKey(
        Session, on_delete=models.CASCADE, related_name="transcripts"
    )
    audio_url = models.CharField(max_length=500)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}:{}".format(str(self.session.session_id), str(self.created))


class Reply(models.Model):
    session = models.ForeignKey(
        Session, on_delete=models.CASCADE, related_name="replies"
    )
    audio_url = models.CharField(max_length=500)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}:{}".format(str(self.session.session_id), str(self.created))
