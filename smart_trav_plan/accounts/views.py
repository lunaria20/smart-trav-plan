from django import forms
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum
from datetime import date

# Import your models (make sure these exist in your models.py)
from smart_trav_plan.SmartTrav.models import Itinerary, Destination, SavedDestination, Expense


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text='Required. Enter a valid email address.',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid credentials. Please try again.")
            return redirect('login')
    return render(request, 'SmartTrav/accounts/login.html')


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created successfully for {username}! Please log in to continue.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'SmartTrav/accounts/signup.html', {'form': form})


@login_required
def dashboard_view(request):
    # Get user's data
    user_itineraries = Itinerary.objects.filter(user=request.user)
    saved_destinations = SavedDestination.objects.filter(user=request.user)
    all_destinations = Destination.objects.all()
    expenses = Expense.objects.filter(itinerary__user=request.user)

    # Calculate stats
    itinerary_count = user_itineraries.count()
    saved_count = saved_destinations.count()
    total_budget = user_itineraries.aggregate(Sum('budget'))['budget__sum'] or 0
    upcoming_trips = user_itineraries.filter(start_date__gte=date.today()).count()

    # Recent itineraries (last 3)
    recent_itineraries = user_itineraries[:3]

    context = {
        'itinerary_count': itinerary_count,
        'saved_count': saved_count,
        'total_budget': total_budget,
        'upcoming_trips': upcoming_trips,
        'recent_itineraries': recent_itineraries,
        'all_itineraries': user_itineraries,
        'destinations': all_destinations,
        'saved_destinations': saved_destinations,
        'expenses': expenses,
    }

    return render(request, 'SmartTrav/accounts/dashboard.html', context)


@login_required
def create_itinerary(request):
    if request.method == 'POST':
        Itinerary.objects.create(
            user=request.user,
            title=request.POST.get('title'),
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date'),
            budget=request.POST.get('budget'),
            notes=request.POST.get('notes', '')
        )
        messages.success(request, 'Itinerary created successfully!')
    return redirect('dashboard')


@login_required
def add_expense(request):
    if request.method == 'POST':
        itinerary = get_object_or_404(Itinerary, id=request.POST.get('itinerary'), user=request.user)
        Expense.objects.create(
            itinerary=itinerary,
            category=request.POST.get('category'),
            description=request.POST.get('description'),
            amount=request.POST.get('amount'),
            date=request.POST.get('date')
        )
        messages.success(request, 'Expense added successfully!')
    return redirect('dashboard')


@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        user.email = request.POST.get('email', user.email)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.save()
        messages.success(request, 'Profile updated successfully!')
    return redirect('dashboard')


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')

def about_view(request):
    return render(request, 'SmartTrav/accounts/about.html')

def service_view(request):
    return render(request, 'SmartTrav/accounts/service.html')

class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "You have been logged out successfully.")
        return super().dispatch(request, *args, **kwargs)



