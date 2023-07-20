from django.db import models

# Create your models here.


class Session(models.Model):
    session_id = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}:{}'.format(str(self.session_id), str(self.created))
