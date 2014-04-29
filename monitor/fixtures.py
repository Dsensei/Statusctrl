import schedule

from monitor.models import Module
from tools.models import WebsiteWatcher, MonitorTool
from django.core.exceptions import ObjectDoesNotExist


try:
    m = Module.objects.get(name="EpiPortal")
except ObjectDoesNotExist:
    m = Module()
    m.name = "EpiPortal"
    m.description = "Web service for students"
    m.hostname = "epiportal.com"
    m.save()

monitors = {
    'tools':
        {
            'AVAILABILITY':
            {
                'description': 'Availability'
            },
            'PING':
            {
                'description': 'Ping'
            }
        }
}
for tool in monitors['tools']:

    try:
        t = MonitorTool.objects.get(name=tool)
    except ObjectDoesNotExist:
        t = MonitorTool()
        t.name = tool
        t.description = monitors['tools'][tool]['description']
        t.save()

try:
    w1 = WebsiteWatcher.objects.get(name="Website watcher 1")
except ObjectDoesNotExist:
    w1 = WebsiteWatcher()
    w1.name = "Website watcher 1"
    w1.description = "watcher for epiportal"
    w1.hostname = "http://epiportal.com"
    w1.ip = "5.135.158.104"
    w1.port = 80
    w1.module = m
    w1.ttl = 10
    w1.save()
    w1.monitor_tools.add(MonitorTool.get('AVAILABILITY'))
    w1.monitor_tools.add(MonitorTool.get('PING'))
    w1.save()

try:
    w2 = WebsiteWatcher.objects.get(name="Website watcher 2")
except ObjectDoesNotExist:
    w2 = WebsiteWatcher()
    w2.name = "Website watcher 2"
    w2.description = "watcher for juliendubiel.net"
    w2.hostname = "http://juliendubiel.net"
    w2.port = 80
    w2.module = m
    w2.ttl = 10
    w2.save()
    w2.monitor_tools.add(MonitorTool.get('AVAILABILITY'))
    w2.monitor_tools.add(MonitorTool.get('PING'))
    w2.save()

watchers = WebsiteWatcher.objects.all()
for watcher in watchers:
    watcher.run(schedule)
# w.run(schedule)
while True:
    schedule.run_pending()