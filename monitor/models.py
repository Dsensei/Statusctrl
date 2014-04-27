from datetime import datetime
from django.db import models
from django.core.validators import URLValidator

from uuidfield import UUIDField


class Module():
    uuid = UUIDField(auto=True, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    date_created = models.DateTimeField(default=datetime.now())
    last_updated = models.DateTimeField(default=datetime.now())
    hostname = models.TextField(validators=[URLValidator()])
