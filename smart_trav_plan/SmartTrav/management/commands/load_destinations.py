from django import forms
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum, Count, Q # Import Q for filtering
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
        input_value = request.POST.get("email", "").strip().lower()
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
    # Get the active section from URL parameter
    active_section = request.GET.get('section', 'overview')

    # Get user's itineraries, SORTED OLDEST TO NEWEST (Requested Change 1)
    user_itineraries = Itinerary.objects.filter(user=request.user).annotate(
        destination_count=Count('itinerary_destinations')
    ).order_by('start_date') # Explicitly sort by start_date

    # --- Destination Search/Filter Logic (Requested Change 2) ---
    query = request.GET.get('q', '').strip()
    active_category = request.GET.get('category', '')

    # Start with all destinations
    all_destinations = Destination.objects.all()

    # Apply search filter if query exists: ONLY FILTER BY NAME (Requested Change 2)
    if query:
        # Use icontains for a flexible match on the destination name
        all_destinations = all_destinations.filter(Q(name__icontains=query))

    # Apply category filter if selected (applied AFTER search filter)
    if active_category:
        all_destinations = all_destinations.filter(category=active_category)
    # -----------------------------------------------------------

    saved_destinations = SavedDestination.objects.filter(user=request.user)
    expenses = Expense.objects.filter(itinerary__user=request.user)

    # Calculate stats
    itinerary_count = user_itineraries.count()
    saved_count = saved_destinations.count()
    total_budget = user_itineraries.aggregate(Sum('budget'))['budget__sum'] or 0
    upcoming_trips = user_itineraries.filter(start_date__gte=date.today()).count()

    # Recent itineraries (first 3, automatically oldest due to sorting)
    recent_itineraries = user_itineraries[:3]

    context = {
        'itinerary_count': itinerary_count,
        'saved_count': saved_count,
        'total_budget': total_budget,
        'upcoming_trips': upcoming_trips,
        'recent_itineraries': recent_itineraries,
        'all_itineraries': user_itineraries,
        'destinations': all_destinations,
        'active_category': active_category,
        'active_section': active_section,
        'saved_destinations': saved_destinations,
        'expenses': expenses,
        'query': query, # Pass the query back to the template
    }
    return render(request, 'SmartTrav/accounts/dashboard.html', context)


@never_cache
@login_required
def create_itinerary(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        budget = request.POST.get('budget')
        notes = request.POST.get('notes', '')

        # --- VALIDATION: Itinerary can only be created if the data is not before today. ---
        try:
            start_date_obj = date.fromisoformat(start_date_str)
            if start_date_obj < date.today():
                messages.error(request, "Start date cannot be in the past. Please choose today or a future date.")
                return redirect('dashboard')
        except (ValueError, TypeError):
            # This handles cases where date strings are malformed or missing (though required in template)
            messages.error(request, "Invalid or missing date submitted.")
            return redirect('dashboard')
        # -----------------------------------------------------------------------------------

        Itinerary.objects.create(
            user=request.user,
            title=title,
            start_date=start_date_str,
            end_date=end_date_str,
            budget=budget,
            notes=notes
        )
        messages.success(request, 'Itinerary created successfully!')
        return redirect('dashboard')

    # If GET, or if validation fails, it redirects to dashboard.
    return redirect('dashboard')


# UPDATED: Itinerary Edit View (Uses dedicated edit_itinerary.html)
@login_required
def edit_itinerary(request, itinerary_id):
    itinerary = get_object_or_404(Itinerary, id=itinerary_id, user=request.user)

    if request.method == 'POST':
        start_date_str = request.POST.get('start_date')

        # --- VALIDATION: Ensure updated start date is not before today ---
        try:
            start_date_obj = date.fromisoformat(start_date_str)
            if start_date_obj < date.today():
                messages.error(request, "Start date cannot be in the past. Please choose today or a future date.")
                # Redirect back to the edit page with the error
                return render(request, 'SmartTrav/accounts/edit_itinerary.html', {'itinerary': itinerary})
        except (ValueError, TypeError):
            messages.error(request, "Invalid or missing date submitted.")
            return render(request, 'SmartTrav/accounts/edit_itinerary.html', {'itinerary': itinerary})
        # ----------------------------------------------------------------

        itinerary.title = request.POST.get('title')
        itinerary.start_date = start_date_str
        itinerary.end_date = request.POST.get('end_date')
        itinerary.budget = request.POST.get('budget')
        itinerary.notes = request.POST.get('notes', '')
        itinerary.save()
        messages.success(request, 'Itinerary updated successfully!')
        return redirect('dashboard')

    return render(request, 'SmartTrav/accounts/edit_itinerary.html', {'itinerary': itinerary})


@login_required
def delete_itinerary(request, itinerary_id):
    itinerary = get_object_or_404(Itinerary, id=itinerary_id, user=request.user)
    if request.method == 'POST':
        itinerary.delete()
        messages.success(request, f'Itinerary "{itinerary.title}" deleted successfully.')
    return redirect('dashboard')


@login_required
def save_destination(request, destination_id):
    destination = get_object_or_404(Destination, id=destination_id)
    if request.method == 'POST':
        # Check if already saved
        if not SavedDestination.objects.filter(user=request.user, destination=destination).exists():
            SavedDestination.objects.create(user=request.user, destination=destination)
            messages.success(request, f'Destination "{destination.name}" saved successfully!')
        else:
            messages.info(request, f'Destination "{destination.name}" is already in your saved list.')

    return redirect('dashboard')


@login_required
def remove_saved_destination(request, destination_id):
    destination = get_object_or_404(Destination, id=destination_id)
    if request.method == 'POST':
        saved_destination = get_object_or_404(SavedDestination, user=request.user, destination=destination)
        saved_destination.delete()
        messages.success(request, f'Destination "{destination.name}" removed from saved list.')

    return redirect('dashboard')


@login_required
def add_destination_to_trip(request):
    if request.method == 'POST':
        destination_id = request.POST.get('destination_id')
        itinerary_id = request.POST.get('itinerary_id')

        destination = get_object_or_404(Destination, id=destination_id)
        itinerary = get_object_or_404(Itinerary, id=itinerary_id, user=request.user)

        # Check if the destination is already linked to the itinerary
        if not ItineraryDestination.objects.filter(itinerary=itinerary, destination=destination).exists():
            ItineraryDestination.objects.create(itinerary=itinerary, destination=destination)
            messages.success(request, f'"{destination.name}" added to itinerary "{itinerary.title}"!')
        else:
            messages.info(request, f'"{destination.name}" is already in itinerary "{itinerary.title}".')

    return redirect('dashboard')


@login_required
def add_expense(request):
    if request.method == 'POST':
        itinerary_id = request.POST.get('itinerary_id')
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        category = request.POST.get('category')
        date_str = request.POST.get('date')

        itinerary = get_object_or_404(Itinerary, id=itinerary_id, user=request.user)

        # Create the expense
        Expense.objects.create(
            itinerary=itinerary,
            description=description,
            amount=amount,
            category=category,
            date=date_str
        )
        messages.success(request, 'Expense added successfully!')
        return redirect('dashboard')

    return redirect('dashboard')  # Fallback


@login_required
def update_profile(request):
    user = request.user
    if request.method == 'POST':
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