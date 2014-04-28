from datetime import datetime
from django.db import models
from django.core.validators import URLValidator
from tools import availability, ping
from monitor.models import Module


class Watcher(models.Model):
    # Seconds between two updates
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    ttl = models.PositiveIntegerField()
    hostname = models.TextField(validators=[URLValidator()], null=True)
    ip = models.GenericIPAddressField(protocol='IPv4', null=True)
    port = models.IntegerField(max_length=5, null=True)
    module = models.ForeignKey(Module)

    def __str__(self):
        return self.url()

    def url(self):
        if self.hostname:
            name = self.hostname
        elif self.ip:
            name = self.ip
        else:
            return ''
        if self.port:
            name = name + ':' + str(self.port)
        return name


class WebsiteWatcher(Watcher):
    def __init__(self):
        super().__init__()

    def run(self, schedule):
        schedule.every(self.ttl).seconds.do(self.update)

    def update(self):
        print("Update")
        if self.update_availability():
            self.update_ping()
        self.module.last_updated = datetime.now()

    def update_availability(self):
        try:
            a = availability.is_up(self.url())
        except (availability.InternetNotReachable,
                availability.InvalidHostname) as err:
            print("Error occured :", err)
            return False
        if a:
            val = 1
        else:
            val = 0
        data = Data()
        data.value = val
        data.watcher = self
        data.save()
        return a

    def update_ping(self):
        p = ping.ping(self.url())
        data = Data()
        data.value = p.avg_rtt
        data.watcher = self
        data.save()
        return data.value

class Data(models.Model):
    date_created = models.DateTimeField(default=datetime.now())
    value = models.DecimalField(max_digits=9, decimal_places=3)
    watcher = models.ForeignKey(Watcher)

