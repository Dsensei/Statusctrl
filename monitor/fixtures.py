import schedule

from monitor.models import Module, WebsiteWatcher, MonitorTool, WatcherOrder
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

try:
    User.objects.get(username='john')
except ObjectDoesNotExist:
    user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')


try:
    m1 = Module.objects.get(name="EpiPortal")
except ObjectDoesNotExist:
    m1 = Module()
    m1.name = "EpiPortal"
    m1.hostname = "epiportal.com"
    m1.description = "Web service for students"
    m1.display_pos = 1
    m1.save()
try:
    m2 = Module.objects.get(name="Julien Dubiel")
except ObjectDoesNotExist:
    m2 = Module()
    m2.name = "Julien Dubiel"
    m2.hostname = "juliendubiel.net"
    m2.description = "Personal website"
    m2.display_pos = 2
    m2.save()

try:
    m3 = Module.objects.get(name="42Portal")
except ObjectDoesNotExist:
    m3 = Module()
    m3.name = "42Portal"
    m3.hostname = "42portal.com"
    m3.description = "Various stuff website"
    m3.display_pos = 3
    m3.save()

try:
    m4 = Module.objects.get(name="Epirev")
except ObjectDoesNotExist:
    m4 = Module()
    m4.name = "Epirev"
    m4.hostname = "epirev.com"
    m4.description = "EPITA's oculus rift association"
    m4.display_pos = 4
    m4.save()

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
            },
            'STATUS':
            {
                'description': 'Status'
            },
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
    w1 = WebsiteWatcher.objects.get(name="epiportal.com")
except ObjectDoesNotExist:
    w1 = WebsiteWatcher()
    w1.ip = "5.135.158.104"
    w1.name = "epiportal.com"
    w1.description = "Main app"
    w1.hostname = "http://epiportal.com"
    w1.port = 80
    w1.module = m1
    w1.ttl = 10
    w1.save()
    WatcherOrder.objects.create(watcher=w1, tool=MonitorTool.get('AVAILABILITY'), display_pos=1)
    WatcherOrder.objects.create(watcher=w1, tool=MonitorTool.get('PING'), display_pos=2)
    WatcherOrder.objects.create(watcher=w1, tool=MonitorTool.get('STATUS'), display_pos=3)
    # w1.monitor_tools.add(MonitorTool.get('AVAILABILITY'))
    # w1.monitor_tools.add(MonitorTool.get('PING'))
    # w1.monitor_tools.add(MonitorTool.get('STATUS'))

    w1.save()

try:
    w2 = WebsiteWatcher.objects.get(name="juliendubiel.net")
except ObjectDoesNotExist:
    w2 = WebsiteWatcher()
    w2.ip = "5.135.158.104"
    w2.name = "juliendubiel.net"
    w2.description = "Home page"
    w2.hostname = "http://juliendubiel.net"
    w2.port = 80
    w2.module = m2
    w2.ttl = 10
    w2.save()
    w2.save()
    WatcherOrder.objects.create(watcher=w2, tool=MonitorTool.get('STATUS'), display_pos=1)

try:
    w3 = WebsiteWatcher.objects.get(name="blog.juliendubiel.net")
except ObjectDoesNotExist:
    w3 = WebsiteWatcher()
    w3.ip = "5.135.158.104"
    w3.name = "blog.juliendubiel.net"
    w3.description = "Personal blog"
    w3.hostname = "http://blog.juliendubiel.net"
    w3.port = 80
    w3.module = m2
    w3.ttl = 10
    w3.save()
    WatcherOrder.objects.create(watcher=w3, tool=MonitorTool.get('AVAILABILITY'), display_pos=1)
    WatcherOrder.objects.create(watcher=w3, tool=MonitorTool.get('PING'), display_pos=2)
    WatcherOrder.objects.create(watcher=w3, tool=MonitorTool.get('STATUS'), display_pos=3)

try:
    w4 = WebsiteWatcher.objects.get(name="dcipher.juliendubiel.net")
except ObjectDoesNotExist:
    w4 = WebsiteWatcher()
    w4.ip = "5.135.158.104"
    w4.name = "dcipher.juliendubiel.net"
    w4.description = "Dcipher project website"
    w4.hostname = "http://dcipher.juliendubiel.net"
    w4.port = 80
    w4.module = m2
    w4.ttl = 10
    w4.save()
    WatcherOrder.objects.create(watcher=w4, tool=MonitorTool.get('STATUS'), display_pos=1)

try:
    w5 = WebsiteWatcher.objects.get(name="paste.42portal.com")
except ObjectDoesNotExist:
    w5 = WebsiteWatcher()
    w5.ip = "5.135.158.104"
    w5.name = "paste.42portal.com"
    w5.description = "Paste system"
    w5.hostname = "http://paste.42portal.com"
    w5.port = 80
    w5.module = m3
    w5.ttl = 10
    w5.save()
    WatcherOrder.objects.create(watcher=w5, tool=MonitorTool.get('AVAILABILITY'), display_pos=3)
    WatcherOrder.objects.create(watcher=w5, tool=MonitorTool.get('PING'), display_pos=2)
    WatcherOrder.objects.create(watcher=w5, tool=MonitorTool.get('STATUS'), display_pos=1)

try:
    w6 = WebsiteWatcher.objects.get(name="epirev.com")
except ObjectDoesNotExist:
    w6 = WebsiteWatcher()
    w6.ip = "37.59.62.110"
    w6.name = "epirev.com"
    w6.description = "Website of EPIREV"
    w6.hostname = "http://epirev.com"
    w6.port = 80
    w6.module = m4
    w6.ttl = 10
    w6.save()
    WatcherOrder.objects.create(watcher=w6, tool=MonitorTool.get('AVAILABILITY'), display_pos=2)
    WatcherOrder.objects.create(watcher=w6, tool=MonitorTool.get('PING'), display_pos=3)
    WatcherOrder.objects.create(watcher=w6, tool=MonitorTool.get('STATUS'), display_pos=1)



watchers = WebsiteWatcher.objects.all()
for watcher in watchers:
    watcher.run(schedule)
while True:
    schedule.run_pending()