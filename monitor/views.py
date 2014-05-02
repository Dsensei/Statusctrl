from datetime import datetime, timedelta
from django.forms import ModelForm

from django.shortcuts import render, redirect, get_object_or_404
from django.template import Context
from django.contrib.auth.decorators import login_required

from monitor.models import Module, Watcher, WebsiteWatcher
from tools import serializer


# Public & Login views
def monitor(request, slug=None):

    authenticated = request.user.is_authenticated()

    one_hour_ago = datetime.today() - timedelta(hours=1)
    one_day_ago = datetime.today() - timedelta(hours=24)
    one_week_ago = datetime.today() - timedelta(hours=168)
    one_month_ago = datetime.today() - timedelta(hours=720)
    if slug:
        module = get_object_or_404(Module, slug_name=slug)
        data = serializer.get_modules(module.slug_name, start=one_day_ago)
    else:
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

class ModuleForm(ModelForm):
    class Meta:
        model = Module

@login_required
def create_module(request):
    form = ModuleForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('monitor')
    return render(request, 'modules/module_form.html', {'form':form})

@login_required
def edit_module(request, slug):
    server = get_object_or_404(Module, slug_name=slug)
    form = ModuleForm(request.POST or None, instance=server)
    if form.is_valid():
        form.save()
        return redirect('monitor')
    return render(request, 'modules/module_form.html', {'form':form})

@login_required
def delete_module(request, slug):
    server = get_object_or_404(Module, slug_name=slug)
    if request.method=='POST':
        server.delete()
        return redirect('monitor')
    return render(
        request,
        'modules/module_confirm_delete.html',
        {'object':server}
    )

class WatcherForm(ModelForm):
    class Meta:
        model = WebsiteWatcher

@login_required
def create_watcher(request):
    form = WatcherForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('monitor')
    return render(request, 'modules/module_form.html', {'form':form})

@login_required
def edit_watcher(request, slug):
    server = get_object_or_404(WebsiteWatcher, slug_name=slug)
    form = WatcherForm(request.POST or None, instance=server)
    if form.is_valid():
        form.save()
        return redirect('monitor')
    return render(request, 'modules/module_form.html', {'form':form})

@login_required
def delete_watcher(request, slug):
    server = get_object_or_404(WebsiteWatcher, slug_name=slug)
    if request.method=='POST':
        server.delete()
        return redirect('monitor')
    return render(
        request,
        'modules/module_confirm_delete.html',
        {'object':server}
    )