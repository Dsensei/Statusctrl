from datetime import datetime
from django.db import models
from django.core.validators import URLValidator

from uuidfield import UUIDField


class Module(models.Model):
    uuid = UUIDField(auto=True, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    date_created = models.DateTimeField(default=datetime.now())
    last_updated = models.DateTimeField(default=datetime.now())
    hostname = models.TextField(validators=[URLValidator()], null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.last_updated = datetime.now()
        super(Module, self).save(*args, **kwargs)
