from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from monitor.models import Module


def add_module(request, name, description=None, hostname=None, public=True):
    try:
        Module.objects.get(name=name)
        return False
    except ObjectDoesNotExist:
        m = Module()
        m.name = name
        m.description = description
        m.hostname = hostname
        m.public = public
        m.save()
        return True

def change_module(request, name, description=None, hostname=None, public=True):
    try:
        m = Module.objects.get(name=name)
        m.description = description
        m.hostname = hostname
        m.save()
        return True
    except ObjectDoesNotExist:
        raise Http404()

def delete_module(request, name):
    try:
        m = Module.objects.get(name=name)
        m.delete()
    except ObjectDoesNotExist:
        raise Http404()