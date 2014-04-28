from datetime import datetime
from django.db import models
from tools import availability, ping
from monitor.models import Module
from django.core.validators import URLValidator
from django.core.validators import MaxValueValidator, MinValueValidator

from uuidfield import UUIDField


class MonitorTool(models.Model):
    uuid = UUIDField(auto=True, unique=True)
    name = models.CharField(max_length=15)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def update(self, watcher):
        if self.name == 'AVAILABILITY':
            self.update_availability(watcher)
        elif self.name == 'PING':
            self.update_ping(watcher)

    def update_availability(self, watcher):
        try:
            a = availability.is_up(watcher)
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
        data.monitor = self
        data.date_created = datetime.now()
        data.save()
        return a

    def update_ping(self, watcher):
        p = ping.ping(watcher.url())
        data = Data()
        data.value = p.avg_rtt
        data.monitor = self
        data.date_created = datetime.now()
        data.save()
        return data.value

    @staticmethod
    def get(name):
        try:
            t = MonitorTool.objects.get(name=name)
            return t
        except:
            return None

    @staticmethod
    def get_all():
        return MonitorTool.objects.all()


class Data(models.Model):
    date_created = models.DateTimeField()
    value = models.DecimalField(max_digits=9, decimal_places=3)
    monitor = models.ForeignKey(MonitorTool)


class Watcher(models.Model):
    # Seconds between two updates
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    ttl = models.PositiveIntegerField()
    hostname = models.TextField(validators=[URLValidator()], null=True)
    ip = models.GenericIPAddressField(protocol='IPv4', null=True)
    port = models.IntegerField(
        max_length=5,
        null=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(65535)
        ]
    )
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
        return name

    def complete_url(self):
        if self.port:
            return self.url() + ':' + str(self.port)
        else:
            return self.url()


class WebsiteWatcher(Watcher):
    monitor_tools = models.ManyToManyField(MonitorTool)

    def run(self, schedule):
        schedule.every(self.ttl).seconds.do(self.update)

    def update(self):
        print("Update")
        for tool in self.monitor_tools.all():
            tool.update(self)
        self.module.last_updated = datetime.now()
        self.module.save()