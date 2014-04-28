from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.template import Context
from tools.models import Watcher, Data
from monitor.models import Module
from tools import serializer

def introduction(request):
    return render(request, 'introduction.html')

def monitor(request, module=None):
    if module:
        try:
            module = Module.objects.get(name=module)
            data = serializer.get_modules(module)
        except ObjectDoesNotExist:
            raise Http404()
    else:
        data = serializer.get_modules()
    return render(request, 'status.html', Context({
        'modules': data,
        }))

def help(request):
    return render(request, 'help.html')

def contribute(request):
    return render(request, 'contribute.html')