from datetime import datetime, timedelta
from django.forms import ModelForm

from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.template import Context
from django.contrib.auth.decorators import login_required, permission_required

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
def edit_module(request, pk):
    server = get_object_or_404(Module, pk=pk)
    form = ModuleForm(request.POST or None, instance=server)
    if form.is_valid():
        form.save()
        return redirect('monitor')
    return render(request, 'modules/module_form.html', {'form':form})

@login_required
def delete_module(request, pk):
    server = get_object_or_404(Module, pk=pk)
    if request.method=='POST':
        server.delete()
        return redirect('monitor')
    return render(
        request,
        'modules/module_confirm_delete.html',
        {'object':server}
    )