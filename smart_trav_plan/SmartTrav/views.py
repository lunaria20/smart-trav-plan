from django import forms
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum, Count
from datetime import date
from django.views.decorators.cache import never_cache
from .models import Itinerary, Destination, SavedDestination, Expense, ItineraryDestination

# Import your models (make sure these exist in your models.py)
from .models import Itinerary, Destination, SavedDestination, Expense


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
        input_value = request.POST.get("email", "").strip().lower()  # Normalize: strip spaces, lowercase
        password = request.POST.get("password")

        user = None

        # Check if input looks like an email (contains '@')
        if '@' in input_value:
            # Try email query first (case-insensitive)
            email_users = User.objects.filter(email__iexact=input_value)
            if email_users.exists():
                user = email_users.first()

        # Fallback to username query
        if not user:
            username_users = User.objects.filter(username__iexact=input_value)
            if username_users.exists():
                user = username_users.first()
            else:
                # Also try standard authenticate (in case it's treated as username)
                user = authenticate(request, username=input_value, password=password)

        # Check password if user found
        if user and user.check_password(password):
            login(request, user)
            messages.success(request, "Login successful! Welcome back.")
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


@never_cache
@login_required
def dashboard_view(request):
    # Get user's data with destination count annotation
    user_itineraries = Itinerary.objects.filter(user=request.user).annotate(
        destination_count=Count('itinerary_destinations')
    )

    saved_destinations = SavedDestination.objects.filter(user=request.user)

    # Filter destinations by category if provided
    active_category = request.GET.get('category', '')
    if active_category:
        all_destinations = Destination.objects.filter(category=active_category)
    else:
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
        'active_category': active_category,  # For filter chips
        'saved_destinations': saved_destinations,
        'expenses': expenses,
    }

    return render(request, 'SmartTrav/accounts/dashboard.html', context)


@never_cache
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


# UPDATED: Itinerary Edit View (Uses dedicated edit_itinerary.html)
@login_required
def edit_itinerary(request, itinerary_id):
    itinerary = get_object_or_404(Itinerary, id=itinerary_id, user=request.user)

    if request.method == 'POST':
        itinerary.title = request.POST.get('title')
        itinerary.start_date = request.POST.get('start_date')
        itinerary.end_date = request.POST.get('end_date')
        itinerary.budget = request.POST.get('budget')
        itinerary.notes = request.POST.get('notes', '')
        itinerary.save()
        messages.success(request, f'Itinerary "{itinerary.title}" updated successfully!')
        return redirect('dashboard')

    # Handle GET request: Render the edit page with existing data
    context = {
        'itinerary': itinerary
    }
    return render(request, 'SmartTrav/accounts/edit_itinerary.html', context)


# Delete Itinerary View
@login_required
def delete_itinerary(request, itinerary_id):
    itinerary = get_object_or_404(Itinerary, id=itinerary_id, user=request.user)

    if request.method == 'POST':
        title = itinerary.title
        itinerary.delete()
        messages.success(request, f'Itinerary "{title}" deleted successfully.')
    return redirect('dashboard')


@never_cache
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
@never_cache
def add_destination_to_trip(request):
    if request.method == 'POST':
        destination_id = request.POST.get('destination_id')
        itinerary_id = request.POST.get('itinerary_id')

        destination = get_object_or_404(Destination, id=destination_id)
        itinerary = get_object_or_404(Itinerary, id=itinerary_id, user=request.user)

        # Check if already added
        if ItineraryDestination.objects.filter(itinerary=itinerary, destination=destination).exists():
            messages.warning(request, f'{destination.name} is already in {itinerary.title}')
        else:
            ItineraryDestination.objects.create(
                itinerary=itinerary,
                destination=destination
            )
            messages.success(request, f'{destination.name} added to {itinerary.title}!')

    return redirect('dashboard')


@login_required
@never_cache
def save_destination(request, destination_id):
    if request.method == 'POST':
        destination = get_object_or_404(Destination, id=destination_id)

        saved, created = SavedDestination.objects.get_or_create(
            user=request.user,
            destination=destination
        )

        if created:
            messages.success(request, f'{destination.name} saved to your favorites!')
        else:
            messages.info(request, f'{destination.name} is already in your favorites.')

    return redirect('dashboard')


@login_required
@never_cache
def remove_saved_destination(request, destination_id):
    if request.method == 'POST':
        # Find the specific SavedDestination instance for the current user and destination
        saved_destination = get_object_or_404(
            SavedDestination,
            user=request.user,
            destination__id=destination_id
        )
        destination_name = saved_destination.destination.name

        # Delete the saved instance
        saved_destination.delete()
        messages.success(request, f'"{destination_name}" removed from your saved places.')

    return redirect('dashboard')


@never_cache
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


@login_required
def itinerary_detail(request, itinerary_id):
    itinerary = get_object_or_404(Itinerary, id=itinerary_id, user=request.user)
    # Fetch all destinations linked to the trip via the intermediary model
    itinerary_destinations = ItineraryDestination.objects.filter(itinerary=itinerary).select_related('destination')

    context = {
        'itinerary': itinerary,
        'itinerary_destinations': itinerary_destinations,
    }
    return render(request, 'SmartTrav/accounts/itinerary_detail.html', context)


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')


def about_view(request):
    return render(request, 'SmartTrav/accounts/about.html')


def service_view(request):
    return render(request, 'SmartTrav/accounts/service.html')


def contact_view(request):
    return render(request, 'SmartTrav/accounts/contact.html')


class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "You have been logged out successfully.")
        return super().dispatch(request, *args, **kwargs)