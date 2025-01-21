from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .forms import UserRegistrationForm, CustomUserForm
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login as auth_login
from django.utils.encoding import force_bytes
from django.contrib.auth.decorators import login_required
from orders.models import LogisticsWorker  # Assuming the model is in the same app

User = get_user_model()

# Register view: Handles user registration and sending activation email
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account until email verification
            user.save()

            # Send activation email
            current_site = get_current_site(request)
            mail_subject = "Activate your user account"
            message = render_to_string("yuzzaz/activate_account.html", {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                'protocol': 'https' if request.is_secure() else 'http',
            })
            email = EmailMessage(mail_subject, message, to=[user.email])
            email.content_subtype = "html"  # Ensure the email content type is HTML
            email.send()

            messages.success(
                request, f"Dear {user.first_name}, please confirm your email to complete registration.")
            return redirect('login')  # Redirect to login page
    else:
        form = UserRegistrationForm()

    return render(request, 'yuzzaz/register.html', {'form': form})


# Activate view: Handles the account activation via the token
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Thank you for confirming your email. You can now log in.")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid.")
        return redirect('homepage')


# Login view: Handles user login after activation
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Search by email instead of username
        user = User.objects.filter(email=username).first()  # email used as username
        if user is not None and user.check_password(password):
            auth_login(request, user)
            messages.success(request, "You have successfully logged in.")
            
            # Redirect the user based on whether they are a logistics worker
            if hasattr(user, 'logisticsworker'):  # Check if the user is a logistics worker
                return redirect('logistics_dashboard')  # Redirect logistics worker to their dashboard
            # return redirect('dashboard')  # Redirect normal user to their dashboard
            return redirect('../orders/user-dashboard')  # Redirect normal user to their dashboard
        else:
            messages.error(request, "Invalid credentials, please try again.")

    return render(request, 'yuzzaz/login.html')


# Homepage view: Displays a welcome message if user is logged in
def homepage(request):
    if request.user.is_authenticated:
        return render(request, 'yuzzaz/homepage.html', {'user': request.user})
    else:
        return redirect('login')  # Redirect to login if user is not authenticated

@login_required
def dashboard(request):
    user = request.user  # Get the current logged-in user
    if request.method == 'POST':
        form = CustomUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('dashboard')  # Redirect to the same page
    else:
        form = CustomUserForm(instance=user)
    
    return render(request, 'yuzzaz/dashboard.html', {
        'user': user,
        'form': form
    })

# Logout view: Handles user logout
def logout(request):
    auth_logout(request)  # Log out the user
    messages.success(request, "You have successfully logged out.")
    return redirect('homepage')  # Redirect to homepage or another page


