from django.db import models

class Watcher():
    # Tool module types
    SITE = 'SITE'
    SSH = 'SSH'
    GIT = 'GIT'
    TYPE_CHOICES = (
        (SITE, 'Website monitoring'),
        (SSH, 'SSH'),
        (GIT, 'GIT'),
    )
    type = models.CharField(
        max_length=3,
        choices=TYPE_CHOICES
    )

