from django.shortcuts import render

def introduction(request):
    return render(request, 'introduction.html')

def monitor(request):
    return render(request, 'status.html')

def help(request):
    return render(request, 'help.html')

def contribute(request):
    return render(request, 'contribute.html')