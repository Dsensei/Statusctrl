import json
from datetime import datetime, timedelta
from tools.models import Data, MonitorTool, WebsiteWatcher
from operator import attrgetter


def get_monitor_data(monitor, date_start=None, date_end=None):
    if not date_start:
        data = Data.objects.filter(monitor=monitor)
        print('DATA =', data)
    elif date_start and date_end:
        data = Data.objects.filter(
            watcher=monitor,
            date__range=[date_start, date_end]
        )
    else:
        data = Data.objects.filter(
            watcher=monitor,
            date__range=[date_start, datetime.now()]
        )
    data.order_by('date_created')
    return data


def get_wanted_data(data, date_min, date_max, interval=None, nb_val=None):
    data_length = len(data)

    if not date_min:
        date_min = min(data,key=attrgetter('date_created')).date_created
    if not date_max:
        date_max = max(data,key=attrgetter('date_created')).date_created
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


def get_watcher(watcher, start=None, end=None, interval=None, nb_val=None):

    l = []
    monitors = watcher.monitor_tools.all()
    for monitor in monitors:
        data = get_monitor_data(monitors, start, end)
        print("get_monitor_data ->", data)
        if interval or nb_val:
            data = get_wanted_data(data, start, end, interval, nb_val)
            print("get_wanted_data ->", data)
        l.append(
            {
                'id': str(monitor.uuid),
                'name': monitor.name,
                'description': monitor.description,
                "data": data
            }
        )
    return l


# Tests :
"""
from tools.models import WebsiteWatcher
w1 = WebsiteWatcher.objects.get(name="Website watcher 1")
from tools import serializer
serializer.get_watcher(w1)
"""