from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist

from django.db import models
from django.core.validators import URLValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from uuidfield import UUIDField
from tools import availability, ping
from django.template.defaultfilters import slugify



class Module(models.Model):

    uuid = UUIDField(auto=True, unique=True),
    slug_name = models.SlugField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    date_created = models.DateTimeField(default=datetime.now())
    last_updated = models.DateTimeField(default=datetime.now())
    hostname = models.TextField(validators=[URLValidator()], null=True)
    public = models.BooleanField(default=True)
    display_pos = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug_name = slugify(self.name)
        self.last_updated = datetime.now()
        super(Module, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        watchers = Watcher.objects.filter(module=self)
        for watcher in watchers:
            watcher.delete()
        super(Module, self).delete(*args, **kwargs)

    @staticmethod
    def get_all(connected):
        if not connected:
            return Module.objects.filter(public=True)
        else:
            return Module.objects.all()


class MonitorTool(models.Model):
    name = models.CharField(max_length=15, unique=True)
    description = models.CharField(max_length=255)
    public = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def update(self, watcher):
        if self.name == 'AVAILABILITY':
            update_availability(self, watcher)
        elif self.name == 'PING':
            update_ping(self, watcher)

    @staticmethod
    def get(name):
        try:
            t = MonitorTool.objects.get(name=name)
            return t
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_all():
        return MonitorTool.objects.all()


class Watcher(models.Model):
    uuid = UUIDField(auto=True, unique=True)
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

    def delete(self, *args, **kwargs):
        all_data = Data.objects.filter(watcher=self)
        for data in all_data:
            data.delete()
        super(Watcher, self).delete(*args, **kwargs)


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
    monitor_tools = models.ManyToManyField(MonitorTool, through='WatcherOrder')

    def run(self, schedule):
        schedule.every(self.ttl).seconds.do(self.update)

    def update(self):
        print("Update")
        for tool in self.monitor_tools.all():
            tool.update(self)
        self.module.last_updated = datetime.now()
        self.module.save()

class WatcherOrder(models.Model):
    display_pos = models.PositiveIntegerField()
    watcher = models.ForeignKey(WebsiteWatcher)
    tool = models.ForeignKey(MonitorTool)

class Data(models.Model):
    date_created = models.DateTimeField()
    value = models.DecimalField(max_digits=9, decimal_places=3)
    monitor = models.ForeignKey(MonitorTool)
    watcher = models.ForeignKey(Watcher)


def update_availability(monitor_tool, watcher):
    a = None
    try:
        a = availability.is_up(watcher)
    except (availability.InternetNotReachable,
            availability.InvalidHostname) as err:
        print("Error occurred!", err)
    if a:
        val = 100
    else:
        val = 0
    data = Data()
    data.value = val
    data.monitor = monitor_tool
    data.watcher = watcher
    data.date_created = datetime.now()
    data.save()
    return a


def update_ping(MonitorTool, watcher):
    try:
        p = ping.ping(watcher.url())
        data = Data()
        data.value = p.avg_rtt
        data.monitor = MonitorTool
        data.watcher = watcher
        data.date_created = datetime.now()
        data.save()
        return data.value
    except:
        pass