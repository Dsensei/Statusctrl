from datetime import datetime, timedelta

from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.template import Context
from django.contrib.auth.decorators import login_required, permission_required

from monitor import management
from monitor.models import Module
from tools import serializer


# Only public views
def introduction(request):
    return render(request, 'introduction.html', Context(
        {
            'public_modules': Module.get_all(False)
        }
    ))


# Public & Login views
def monitor(request, module=None):

    authenticated = request.user.is_authenticated()

    if module:
        try:
            module = Module.objects.get(slug_name=module)
            data = serializer.get_modules(module.name)
        except ObjectDoesNotExist:
            raise Http404()
    else:
        one_hour_ago = datetime.today() - timedelta(hours=1)
        data = serializer.get_modules(start=one_hour_ago)

    return render(request, 'status.html', Context(
        {
            'modules': data,
            'public_modules': Module.get_all(authenticated)
        }
    ))


def contribute(request):

    authenticated = request.user.is_authenticated()

    return render(request, 'contribute.html', Context(
        {
            'public_modules': Module.get_all(authenticated)
        }
    ))


def status_json(request):

    authenticated = request.user.is_authenticated()

    return render(request, 'status.json', Context(
        {
            'public_modules': Module.get_all(authenticated)
        }
    ))


# Only registration views
@login_required
def help(request):
    return render(request, 'help.html', Context(
        {
            'public_modules': Module.get_all(True)
        }
    ))


@permission_required('monitor.management.add_module')
def add_module(request):
    management.add_module()