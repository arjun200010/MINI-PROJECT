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
            auth_login(request, user)
            request.session['username']=username
            return redirect('loginhome') 
            
            
        else:
            messages.error(request, 'Invalid login credentials.')
            return redirect('login')
    response = render(request,'login.html')
    response['Cache-Control'] = 'no-store, must-revalidate'
    return response

def loginhome(request):
        
        if 'username' in request.session:
            response = render(request, 'loginhome.html')
            response['Cache-Control'] = 'no-store, must-revalidate'
            return response
        else:
            return redirect('login')
def handlelogout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')  



