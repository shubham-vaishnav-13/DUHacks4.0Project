from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model, get_backends
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.utils.timezone import now
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .forms import SignupForm, LoginForm, CustomPasswordResetForm
from .models import Role

User = get_user_model()

#  Home View (Shows home for new users, login if session expired)


def home(request):
    user_email = request.session.get("user_email")

    if user_email:  # If user is logged in, show Home with User Context
        return render(request, "HomePageAuth/home.html", {"user_email": user_email})

    #  Show home page for first-time visitors
    return render(request, "HomePageAuth/home.html")


#  Signup View with Email Verification
def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            role = form.cleaned_data["role"]

            #  Prevent duplicate email registration
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered.")
                return render(request, "HomePageAuth/signup.html", {"form": form})

            #  Generate verification code
            verification_code = get_random_string(
                length=6, allowed_chars="1234567890")

            #  Store verification details in session
            request.session["signup_data"] = {
                "email": email,
                "username": username,
                "password": password,
                "role": role.id,  # Store role ID
                "verification_code": verification_code,
                "expires_at": str(now().timestamp() + 300),  # 5-minute expiry
            }
            request.session.set_expiry(300)  # Session expires in 5 minutes

            #  Send verification email
            send_mail(
                "Verify Your Email - CodeSphere",
                f"Your verification code is {verification_code}. It is valid for 5 minutes.",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            messages.success(
                request, "A verification code has been sent to your email.")
            return redirect("/verify-email/")

    else:
        form = SignupForm()

    return render(request, "HomePageAuth/signup.html", {"form": form})


# Email Verification View
def verify_email(request):
    signup_data = request.session.get("signup_data")

    if not signup_data:
        messages.error(request, "Session expired. Please sign up again.")
        return redirect("/signup/")

    if request.method == "POST":
        entered_code = request.POST.get("verification_code")

        # Check if session expired
        if now().timestamp() > float(signup_data.get("expires_at", 0)):
            messages.error(
                request, "Verification code expired. Please sign up again.")
            request.session.pop("signup_data", None)
            return redirect("/signup/")

        # Check if code matches
        if entered_code != signup_data["verification_code"]:
            messages.error(
                request, "Invalid verification code. Please try again.")
            return render(request, "HomePageAuth/verify_email.html")

        # Get Role Instance and Create User
        role = get_object_or_404(
            Role, id=signup_data["role"])  # Fix for role_id
        user = User.objects.create_user(
            username=signup_data["username"],
            email=signup_data["email"],
            password=signup_data["password"],
            role=role,
        )
        user.is_active = True
        user.save()

        # Get Authentication Backend and Assign to User
        backend = get_backends()[0]  # Use the first available backend
        user.backend = f"{backend.__module__}.{backend.__class__.__name__}"

        # Auto-login User
        login(request, user, backend=user.backend)

        # Remove session data after success
        request.session.pop("signup_data", None)

        messages.success(
            request, "Your email has been verified. You are now logged in.")
        return redirect("/")

    return render(request, "HomePageAuth/verify_email.html")


# Login View with "Remember Me" and Error Handling
def login_view(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)

        # Clear old messages before adding new ones
        storage = messages.get_messages(request)
        storage.used = True

        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            remember_me = form.cleaned_data.get("remember_me")

            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                request.session["user_email"] = user.email

                if remember_me:
                    request.session.set_expiry(1209600)  # 2 weeks expiry
                else:
                    request.session.set_expiry(0)  # Expires on browser close

                messages.success(request, "Login successful!")
                return redirect("/")
            else:
                messages.error(request, "Invalid email or password.")

    return render(request, "HomePageAuth/login.html", {"form": form})


# Logout View
def logout_view(request):
    request.session.flush()  # Clear session
    messages.success(request, "Logged out successfully.")
    return redirect("/")


# Password Reset View (Checks if email exists before sending email)
def password_reset_request(request):
    if request.method == "POST":
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            if not User.objects.filter(email=email).exists():
                messages.error(request, "No account found with this email.")
                return render(request, "registration/password_reset_form.html", {"form": form})

            form.save(
                request=request,
                use_https=True,
                email_template_name="registration/password_reset_email.html",
                subject_template_name="registration/password_reset_subject.txt",
            )

            messages.success(
                request, "If an account exists with this email, a password reset link has been sent.")
            return redirect("password_reset_done")

    else:
        form = CustomPasswordResetForm()

    return render(request, "registration/password_reset_form.html", {"form": form})
