from django.shortcuts import HttpResponse

def index(request):
    return HttpResponse("Index Page")

def download_set(request):
    return HttpResponse("Download Set")

def report(request):
    return HttpResponse("Report")
