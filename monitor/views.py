from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.template import Context
from tools.models import Watcher, Data
from monitor.models import Module

def introduction(request):
    return render(request, 'introduction.html')

def monitor(request, module=None):
    if module:
        try:
            modules = Module.objects.get(name=module)
        except ObjectDoesNotExist:
            raise Http404()
        watchers = Watcher.objects.filter(module=modules)
        datas = Data.objects.filter(watcher__in=watchers)
    else:
        modules = Module.objects.all()
        watchers = Watcher.objects.all()
        datas = Data.objects.all()

    return render(request, 'status.html', Context({
        'modules': modules,
        'watchers': watchers,
        'datas': datas,
        }))

def help(request):
    return render(request, 'help.html')

def contribute(request):
    return render(request, 'contribute.html')