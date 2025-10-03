from django import forms
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

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
        print("POST data:", request.POST)  # Debug line
        form = CustomUserCreationForm(request.POST)
        print("Form is valid:", form.is_valid())  # Debug line
        if form.is_valid():
            print("Email from form:", form.cleaned_data.get('email'))  # Debug line
            user = form.save()
            print("User saved with email:", user.email)  # Debug line
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created successfully for {username}! Please log in to continue.')
            return redirect('login')
        else:
            print("Form errors:", form.errors)  # Debug line
    else:
        form = CustomUserCreationForm()

    return render(request, 'SmartTrav/accounts/signup.html', {'form': form})

def dashboard_view(request):
    return render(request, 'SmartTrav/accounts/dashboard.html')

def logout_view(request):
    return render(request, 'SmartTrav/accounts/logout.html')

class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "You have been logged out successfully.")
        return super().dispatch(request, *args, **kwargs)