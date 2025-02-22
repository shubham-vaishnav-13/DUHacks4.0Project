from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth import authenticate
from .models import User, Role


#  Signup Form with Improved Validation
class SignupForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "class": "border border-gray-300 rounded-lg px-4 py-2 w-full",
            "placeholder": "Enter your email"
        })
    )
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            "class": "border border-gray-300 rounded-lg px-4 py-2 w-full",
            "placeholder": "Enter your username"
        })
    )
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            "class": "border border-gray-300 rounded-lg px-4 py-2 w-full",
            "placeholder": "Enter your password"
        })
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            "class": "border border-gray-300 rounded-lg px-4 py-2 w-full",
            "placeholder": "Confirm your password"
        })
    )
    role = forms.ModelChoiceField(
        queryset=Role.objects.all(),
        empty_label="Select a Role",
        widget=forms.Select(attrs={
            "class": "border border-gray-300 rounded-lg px-4 py-2 w-full",
            "placeholder": "Select a role"
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

    def clean_email(self):
        """  Validate Email Uniqueness """
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "This email is already registered. Please use a different one.")
        return email

    def clean(self):
        """  Ensure Passwords Match """
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error(
                "password2", "Passwords do not match. Please enter the same password.")

        return cleaned_data

    def clean_username(self):
        """  Ensure username is unique """
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "This username is already taken. Choose a different one.")
        return username

    def clean(self):
        """  Check if passwords match """
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error(
                "password2", "Passwords do not match. Please try again.")

        return cleaned_data


#  Login Form with Proper Validation+
class LoginForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "class": "border border-gray-300 rounded-lg px-4 py-2 w-full",
            "placeholder": "Enter your email"
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "border border-gray-300 rounded-lg px-4 py-2 w-full",
            "placeholder": "Enter your password"
        })
    )
    remember_me = forms.BooleanField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                self.add_error("email", "No account found with this email.")
                return

            user = authenticate(username=user.username, password=password)
            if user is None:
                self.add_error(
                    "password", "Incorrect password. Please try again.")

        return cleaned_data


#  Custom Password Reset Form (Checks if Email Exists)
class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "class": "border border-gray-300 rounded-lg px-4 py-2 w-full",
            "placeholder": "Enter your email"
        })
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("No account found with this email.")
        return email
