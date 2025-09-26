from django.shortcuts import render

# Create your views here.
from .models import Destination

def index(request):
    destinations = Destination.objects.all()
    return render(request, "SmartTrav/index.html", {"destinations": destinations})
