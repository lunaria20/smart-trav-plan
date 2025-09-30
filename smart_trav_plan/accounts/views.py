from django.shortcuts import render

def login_view(request):
    return render(request, 'SmartTrav/accounts/login.html')

def signup_view(request):
    return render(request, 'SmartTrav/accounts/signup.html')

def dashboard_view(request):
    return render(request, 'SmartTrav/accounts/dashboard.html')
