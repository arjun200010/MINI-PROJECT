from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth import logout
from django.contrib import messages
from .models import User
from django.contrib.auth.decorators import login_required
import json
from django.shortcuts import get_object_or_404, redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string

def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            # Check if the email is unique
            if not User.objects.filter(email=email).exists():
                # Create a new user
                user = User.objects.create_user(first_name=firstname,last_name=lastname,username=username, email=email,password=password,role="CUSTOMER")
                user.save()
                messages.success(request,"Signup successfull!!!")
                return redirect('login')
            else:
                messages.error(request, 'Email already exists.')
        else:
            messages.error(request, 'Passwords do not match.')
    
    return render(request, 'signup.html')

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Assuming the user's role can be obtained from the user object
            if user.role == "ADMIN":
                auth_login(request, user)  # Log in the user
                request.session['username'] = username
                return redirect("adminfirst")
            elif user.role == "CUSTOMER":
                auth_login(request, user)  # Log in the user
                request.session['username'] = username
                return redirect('loginhome')
            else:
                auth_login(request, user)  # Log in the user
                request.session['username'] = username
                return redirect("vendorhome")
        else:
            messages.error(request, 'Invalid login credentials or account has been deactivated')
            return redirect('login')
    response = render(request, 'login.html')
    response['Cache-Control'] = 'no-store, must-revalidate'
    return response


def loginhome(request):
        
        if 'username' in request.session:
            response = render(request, 'loginhome.html')
            response['Cache-Control'] = 'no-store, must-revalidate'
            return response
        else:
            return redirect('login')
        
def adminfirst(request):
    if 'username' in request.session:
            response = render(request, 'adminfirst.html')
            response['Cache-Control'] = 'no-store, must-revalidate'
            return response
    else:
            return redirect('login')

def vendorhome(request):
    return render(request,"vendorhome.html")


def adminhome(request):
    users = User.objects.all()
    return render(request, 'adminhome.html', {'users': users})


def handlelogout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')  

def check_user_email(request):
    userd = request.GET.get('email')
    data = {
        "exists": User.objects.filter(email=userd).exists()
    }
    return JsonResponse(data)

def deactivate_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.is_active:
        user.is_active = False
        user.save()
         # Send deactivation email
        subject = 'Account Deactivation'
        message = 'Your account has been deactivated by the admin.'
        from_email = 'achu31395@gmail.com'  # Replace with your email
        recipient_list = [user.email]
        html_message = render_to_string('deactivation_email.html', {'user': user})

        send_mail(subject, message, from_email, recipient_list, html_message=html_message)

        messages.success(request, f"User '{user.username}' has been deactivated, and an email has been sent.")
    else:
        messages.warning(request, f"User '{user.username}' is already deactivated.")
    return redirect('adminhome')

def activate_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if not user.is_active:
        user.is_active = True
        user.save()

        # Send activation email
        subject = 'Account Activation'
        message = 'Your account has been activated by the admin.'
        from_email = 'achu31395@gmail.com'  # Replace with your email
        recipient_list = [user.email]
        html_message = render_to_string('activation_email.html', {'user': user})

        send_mail(subject, message, from_email, recipient_list, html_message=html_message)

        messages.success(request, f"User '{user.username}' has been activated, and an email has been sent.")
    else:
        messages.warning(request, f"User '{user.username}' is already active.")
    return redirect('adminhome')



# def edit_user(request, user_id):
#     try:
#         user = User.objects.get(id=user_id)
#         return render(request, 'edit_user.html', {'user': user})
#     except User.DoesNotExist:
#         return HttpResponse("User not found", status=404)
    

# def update_user(request, user_id):
#     try:
#         user = User.objects.get(id=user_id)
        
#         if request.method == 'POST':
#                     user.username = request.POST.get('username')
#                     user.email = request.POST.get('email')
#                     user.first_name = request.POST.get('first_name')
#                     user.last_name = request.POST.get('last_name')
#                     user.is_active = request.POST.get('is_active') == 'on'
#                     user.role = request.POST.get('role')
#                     user.save()
#                     return redirect('adminhome')
#         return HttpResponse("Invalid request method", status=400)
#     except User.DoesNotExist:
#         return HttpResponse("User not found", status=404)



from django.contrib.auth.hashers import make_password

def create_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        is_active = request.POST.get('is_active') == 'on'
        role = request.POST.get('role')

        # Hash the password before creating the user
        password_hashed = make_password(password)

        user = User.objects.create(
            username=username,
            email=email,
            password=password_hashed,
            first_name=first_name,
            last_name=last_name,
            is_active=is_active
        )
        user.save()
        return redirect('adminhome')

    return render(request, 'create_user.html')



@login_required
def update_profile(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        
        # Update the user's profile data
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.save()
        
        return redirect('login')

    return render(request, 'update_profile.html')


@login_required
def change_password(request):
        if request.method == 'POST':
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            
            user = authenticate(username=request.user.username, password=current_password)
        
            if user is not None:
                # Password is correct
                request.user.set_password(new_password)
                request.user.save()
                # Log the user out for security reasons and then log them back in
                auth_login(request, request.user)
                messages.success(request,"Password changed sucessfully")
                return redirect('login')
            else:
                # Password is incorrect
                messages.error(request,"Incorrect Current password")
                return render(request, 'change_password.html')
    
        return render(request, 'change_password.html')




