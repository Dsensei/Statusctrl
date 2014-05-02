from datetime import datetime, timedelta
from operator import attrgetter

from monitor.models import Module, Data, WebsiteWatcher
from tools import availability


def get_monitor_data(watcher, monitor, date_start=None, date_end=None):

    if not date_start:
        data = Data.objects.filter(monitor=monitor)
    elif date_start and date_end:
        data = Data.objects.filter(
            monitor=monitor,
            watcher=watcher,
            date__range=[date_start, date_end]
        )
    else:
        data = Data.objects.filter(
            monitor=monitor,
            watcher=watcher,
            date_created__range=[date_start, datetime.now()]
        )
    data.order_by('date_created')
    return data


def get_wanted_data(data, date_min, date_max, interval=None, nb_val=None):

    data_length = len(data)

    date_min = min(data, key=attrgetter('date_created')).date_created
    if not date_max:
        date_max = max(data, key=attrgetter('date_created')).date_created
    delta = date_max - date_min

    if nb_val:
        if nb_val > data_length:
            nb_val = data_length
        interval = delta.seconds / nb_val
    elif interval:
        nb_val = delta.seconds / interval

    d_list = [date_max - timedelta(seconds=interval) for x in range(0, nb_val)]

    l = []
    for d in d_list:
        obj = min(data, key=lambda t: abs(d - t.date_created))
        l.append(obj)
    return l


def get_monitors(watcher, start=None, end=None, interval=None, nb_val=None):

    l = []
    monitors = watcher.monitor_tools.all()
    for monitor in monitors:
        data = get_monitor_data(watcher, monitor, start, end)
        if interval or nb_val:
            data = get_wanted_data(data, start, end, interval, nb_val)
        # TODO: Find something speeder
        if len(data) > 0:
            c = 0
            for i in data:
                c += i.value
            avg = float(c) / float(len(data))
        else:
            avg = 0
        l.append(
            {
                'name': monitor.name,
                'description': monitor.description,
                "data": data,
                "data_avg": avg
            }
        )
    return l


def get_watchers(module, start=None, end=None, interval=None, nb_val=None):

    l = []
    watchers = WebsiteWatcher.objects.filter(module=module)
    for watcher in watchers:
        l.append(
            {
                'id': str(watcher.uuid),
                'name': watcher.name,
                'description': watcher.description,
                'ttl': watcher.ttl,
                'url': watcher.url(),
                'port': watcher.port,
                'monitors': get_monitors(watcher, start, end, interval, nb_val)
            }
        )
    return l


def get_module(module, start=None, end=None, interval=None, nb_val=None):
    return (
        {
            'name': module.name,
            'slug': module.slug_name,
            'description': module.description,
            'last_updated': module.last_updated,
            'hostname': module.hostname,
            'url': availability.normalize_url(module.hostname),
            'watchers': get_watchers(module, start, end, interval, nb_val)
        }
    )


def get_modules(module_slug=None, start=None, end=None, interval=None, nb_val=None):

    l = []
    if not module_slug:
        modules = Module.objects.all()
    else:
        modules = Module.objects.filter(slug_name=module_slug)
    for module in modules:
        l.append(get_module(module, start, end, interval, nb_val))
    return l