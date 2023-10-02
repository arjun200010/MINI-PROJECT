from django.shortcuts import render,redirect
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth import logout
from django.contrib import messages
from .models import User
from django.contrib.auth.decorators import login_required
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
                print(firstname,lastname,password,email)
                user = User.objects.create_user(first_name=firstname,last_name=lastname,username=username, email=email,password=password,role="CUSTOMER")
                # user.firstname = firstname

                user.save()
                return redirect('login')
            else:
                messages.error(request, 'Email already exists.')
        else:
            messages.error(request, 'Passwords do not match.')
    
    return render(request, 'signup.html')
#    if request.method == 'POST':
#             # Create the user
#             first_name=request.POST['first-name']
#             username = request.POST['username']  
#             email = request.POST['email']
#             password = request.POST['password']  
#             confirm_password = request.POST['confirm_password']
#             user = User.objects.create_user(first_name=first_name,username=username, email=email, password=password)
#             user.save()
#             return redirect('login')  
#    else:
#         return render(request, 'signup.html')


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")  
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('loginhome')
        else:
            return redirect('login')
    return render(request,"login.html")



def loginhome(request):
    return render(request, 'loginhome.html')

def handlelogout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')  # Replace 'index' with the name of your desired landing page






