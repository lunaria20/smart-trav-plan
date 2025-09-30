from django.shortcuts import render

def index(request):
    return render(request, 'SmartTrav/index.html')
