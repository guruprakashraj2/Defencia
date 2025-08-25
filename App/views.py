from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from .forms import ContactForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import ForgetPasswordForm, ResetPasswordForm

def base(request):
    return render(request,"base.html")
def login_view(request):
    form = LoginForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            auth_login(request, form.user)
            messages.success(request, f"Welcome {form.user.username}, you have successfully logged in.")
            return redirect('App:dashboard')
        else:
            messages.error(request, "Login failed. Please check your credentials.")

    # Always return a response
    return render(request, 'login.html', {'form': form})

def Register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            messages.success(request, "Registered successfully! Redirecting to login page...")
            return render(request, "Register.html", {"form": RegisterForm()})
    else:
        form = RegisterForm()
    return render(request, "Register.html", {"form": form})

def dashboard_view(request):
    return render(request, 'dashboard.html')

def logout(request):
    auth_logout(request)   # always log the user out
    messages.success(request, "✅ You have logged out successfully.")
    return redirect("App:dashboard")
def about(request):
    return render(request, "about.html")

def leadership(request):
    return render(request, "leadership.html")

def vision_mission(request):
    return render(request, "vision_mission.html")
def cybersecurity(request):
    return render(request, "cybersecurity.html")

def webappdevelopment(request):
    return render(request, "webappdevelopment.html")

def penetrationtester(request):
    return render(request, "penetrationtester.html")

def mobiledevelopment(request):
    return render(request, "mobiledevelopment.html")
def jobopenings(request):
    return render(request, "jobopenings.html")

def internships(request):
    return render(request, "internships.html")

def whyjoinus(request):
    return render(request, "whyjoinus.html")
def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # ✅ stores in DB
            messages.success(request, "✅ Your message has been sent successfully!")
            return redirect("App:contact")  # redirect back to contact page
    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})
def forget_password(request):
    form = ForgetPasswordForm()
    if request.method == 'POST':
        form = ForgetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, "No account found with that email address.")
                return redirect('App:forget_password')

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain

            subject = 'Reset Your Password'
            message = render_to_string('reset_password_email.txt', {
    'user': user,
    'domain': domain,
    'uid': uid,
    'token': token,

            })

            send_mail(subject, message, 'your_email@example.com', [email])
            messages.success(request, 'A reset link has been sent to your email.')
            return redirect('App:login')

    return render(request, 'forget_password.html', {'form': form})


def reset_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError, OverflowError):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        form = ResetPasswordForm(request.POST or None)
        if request.method == 'POST' and form.is_valid():
            password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']

            if password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return render(request, 'reset_password.html', {'form': form})

            user.set_password(password)
            user.save()
            messages.success(request, 'Your password has been reset. Please log in.')
            return redirect('App:login')
        return render(request, 'reset_password.html', {'form': form})
    else:
        messages.error(request, 'The password reset link is invalid or has expired.')
        return redirect('App:forget_password')
