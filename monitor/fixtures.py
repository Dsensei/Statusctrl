from monitor.models import Module
from tools.models import WebsiteWatcher, Watcher
import schedule
import time

m = Module()
m.name = "Epiportal"
m.description = "Web service for students"
m.hostname = "epiportal.com"
m.save()

w = WebsiteWatcher()
w.name = "Website watcher"
w.description = "watcher for epiportal - experimental"
w.hostname = "epiportal.com"
w.ip = "5.135.158.104"
w.port = None
w.module = m
w.ttl = 60
w.save()

# watchers = Watcher.objects.all()
# for watcher in watchers:
#     print("Watcher =", watcher)
#     watcher.run(schedule)
w.run(schedule)
while True:
    schedule.run_pending()
    time.sleep(1)