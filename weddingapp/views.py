from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth import logout
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import UserProfile,VendorProfile
from .models import GoldPackage,SilverPackage,PlatinumPackage,CustomisePackage, Notification
from django.contrib.auth.decorators import login_required
import json
from django.shortcuts import get_object_or_404, redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from . import candy



def index(request):
    return candy.render(request, 'index.html')

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
                user = User.objects.create_user(username=username, first_name=firstname, last_name=lastname, email=email, password=password,role="CUSTOMER")

                user.is_active = False  # Deactivate the user until verification
                verification_code = get_random_string(32)  # Generate a random code
                user.verification_code = verification_code
                user.save()

                # Send an email with the verification link
                subject = 'Email Verification'
                verification_url = request.build_absolute_uri(reverse('verify_email', args=[verification_code]))
                message = f'Click the following link to verify your email: {verification_url}'
                from_email = 'achu31395@gmail.com'
                recipient_list = [email]
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                messages.success(request,"An account activation link is send to your email ,verify it to continue")
                return redirect('signup')  # Redirect to a login page with a message

            else:
                # Email already exists
                messages.error(request,"Email already exists")
                return render(request, 'signup.html')
        else:
            # Passwords do not match
            messages.error(request,"Password does not match")
            return render(request, 'signup.html')

    return candy.render(request, 'signup.html')

def vendorsignup(request):
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
                user = User.objects.create_user(username=username, first_name=firstname, last_name=lastname, email=email, password=password,role="VENDOR")

                user.is_active = False  # Deactivate the user until verification
                verification_code = get_random_string(32)  # Generate a random code
                user.verification_code = verification_code
                user.save()

                # Send an email with the verification link
                subject = 'Email Verification'
                verification_url = request.build_absolute_uri(reverse('verify_email', args=[verification_code]))
                message = f'Click the following link to verify your email: {verification_url}'
                from_email = 'achu31395@gmail.com'
                recipient_list = [email]
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                messages.success(request,"An account activation link is send to your email ,verify it to continue")
                return redirect('vendorsignup')  # Redirect to a login page with a message

            else:
                # Email already exists
                messages.error(request,"Email already exists")
                return render(request, 'vendorsignup.html')
        else:
            # Passwords do not match
            messages.error(request,"Password does not match")
            return render(request, 'vendorsignup.html')

    return render(request, 'vendorsignup.html')

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
            messages.error(request, 'Invalid login credentials or account is deactivated')
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
        user_count = User.objects.filter(role='CUSTOMER').count()
        vendor_count = User.objects.filter(role='VENDOR').count()

        # Assuming "active" is a status field in your booking model
        active_booking_count = GoldPackage.objects.filter(is_booked=True).count() + \
                              SilverPackage.objects.filter(is_booked=True).count() + \
                              PlatinumPackage.objects.filter(is_booked=True).count() + \
                              CustomisePackage.objects.filter(is_booked=True).count()
        # Get the three most recent notifications
        notifications = Notification.objects.order_by('-timestamp')[:3]

        context = {
            'user_count': user_count,
            'vendor_count': vendor_count,
            'active_booking_count': active_booking_count,
            'notifications' : notifications
        }

        response = render(request, 'adminfirst.html',context)
        response['Cache-Control'] = 'no-store, must-revalidate'
        return response
    else:
        return redirect('login')


def vendorhome(request):
    if 'username' in request.session:
            response = render(request, 'vendorhome.html')
            response['Cache-Control'] = 'no-store, must-revalidate'
            return response
    else:
            return redirect('login')




def adminhome(request):
    # Fetch all users initially
    users = User.objects.all()

    # Check if a role filter is provided in the URL
    role_filter = request.GET.get('role', '')
    
    if role_filter:
        # Apply role filter if present
        users = users.filter(role=role_filter)

    context = {
        'users': users,
        'messages': [],  # Add your messages here if needed
        'selected_role': role_filter,
    }

    return render(request, 'adminhome.html', context)

from .models import UserProfile
@login_required
def userupdatetable(request):
    user_profiles = UserProfile.objects.all()
    return render(request, 'userupdatetable.html', {'user_profiles': user_profiles})


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

from django.core.exceptions import ObjectDoesNotExist

@login_required
def vendor_update_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        user_profile = UserProfile(user=request.user)
        user_profile.save()

    vendor_profile, created = VendorProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        skill = request.POST.get('skill')
        document = request.FILES.get('document')
        if document and not document.name.endswith('.pdf'):
            messages.error(request, 'Only PDF files are allowed for the document.')
            return redirect('vendor_update_profile') 
        
        # Update VendorProfile fields
        vendor_profile.skill = skill
        vendor_profile.document = document
        vendor_profile.save()
        # Update UserProfile fields
        user = get_object_or_404(User, pk=request.user.id)
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()
        messages.success(request,"Profile Updated")
        return redirect('vendor_update_profile')  # Redirect to a success page

    return render(request, 'vendor_update_profile.html', {'user_profile': user_profile, 'vendor_profile': vendor_profile})



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
        # Update the user's profile data
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        
        return redirect('loginhome')

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

@login_required
def vendor_change_password(request):
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
    
        return render(request, 'vendor_change_password.html')


def verify_email(request, verification_code):
    User = get_user_model()
    
    try:
        user = User.objects.get(verification_code=verification_code, is_active=False)
        user.is_active = True  # Activate the user
        user.is_verified = True  # Set the user as verified
        user.save()
        return redirect('login')
        
    except User.DoesNotExist:
        messages.error(request,"Invalid email.Please enter valid email")
        return render(request, 'signup.html')  # Handle invalid verification codes




from datetime import datetime

from datetime import datetime
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import GoldPackage, SilverPackage, PlatinumPackage, CustomisePackage

@login_required
def gold_booking(request):
    if request.method == 'POST':
        # Retrieve data from the form
        date_of_booking = request.POST.get('date_of_booking')
        destination_selected = request.POST.get('destination_selected')

        # Get the current user (logged-in user)
        current_user = request.user

        # Check if the user already has a confirmed booking in any table
        has_confirmed_booking = (
            GoldPackage.objects.filter(user=current_user, is_booked=True).exists() or
            SilverPackage.objects.filter(user=current_user, is_booked=True).exists() or
            PlatinumPackage.objects.filter(user=current_user, is_booked=True).exists() or
            CustomisePackage.objects.filter(user=current_user, is_booked=True).exists()
        )

        # Get the latest confirmed booking for the user
        latest_confirmed_booking = GoldPackage.objects.filter(
            user=current_user, is_booked=True
        ).order_by('-date_of_booking').first()

        # Check if there is a latest confirmed booking and if its date has not passed yet
        if has_confirmed_booking and latest_confirmed_booking and latest_confirmed_booking.date_of_booking >= datetime.now().date():
            messages.error(request, f"You already have a confirmed booking. Rebooking is not permitted until the date of the latest confirmed booking has passed.")
            return redirect('view_profile')

        # Check if there is a latest confirmed booking and if its date is later than the new booking date
        if latest_confirmed_booking and latest_confirmed_booking.date_of_booking and latest_confirmed_booking.date_of_booking > datetime.strptime(date_of_booking, "%Y-%m-%d").date():
            messages.error(request, f"You already have a confirmed booking with a date later than {date_of_booking}. Rebooking is not permitted until the date of the latest confirmed booking has passed.")
            return redirect('view_profile')

        # Create a new GoldPackage record with the form data and the current user
        gold_package = GoldPackage.objects.create(
            user=current_user,
            date_of_booking=date_of_booking,
            destination_selected=destination_selected,
            is_booked=False  # Set the initial booking status to False
        )

        # Save the GoldPackage record
        gold_package.save()

        # Redirect to a success page for a new booking
        return redirect('confirmation')

    return render(request, 'gold_booking.html')






from datetime import datetime
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import SilverPackage

@login_required
def silver_booking(request):
    if request.method == 'POST':
        # Retrieve data from the form
        date_of_booking = request.POST.get('date_of_booking')
        destination_selected = request.POST.get('destination_selected')
        honeymoon_destination = request.POST.get('honeymoon_destination')

        # Get the current user (logged-in user)
        current_user = request.user

        # Check if the user already has a confirmed booking in any table
        has_confirmed_booking = (
            GoldPackage.objects.filter(user=current_user, is_booked=True).exists() or
            SilverPackage.objects.filter(user=current_user, is_booked=True).exists() or
            PlatinumPackage.objects.filter(user=current_user, is_booked=True).exists() or
            CustomisePackage.objects.filter(user=current_user, is_booked=True).exists()
        )

        latest_confirmed_booking = SilverPackage.objects.filter(
            user=current_user, is_booked=True
        ).order_by('-date_of_booking').first()

        # Check if there is a latest confirmed booking and if its date has not passed yet
        if has_confirmed_booking and latest_confirmed_booking and latest_confirmed_booking.date_of_booking >= datetime.now().date():
            messages.error(request, f"You already have a confirmed booking. Rebooking is not permitted until the date of the latest confirmed booking has passed.")
            return redirect('view_profile')

        # Check if there is a latest confirmed booking and if its date is later than the new booking date
        if latest_confirmed_booking and latest_confirmed_booking.date_of_booking > datetime.strptime(date_of_booking, "%Y-%m-%d").date():
            messages.error(request, f"You already have a confirmed booking with a date later than {date_of_booking}. Rebooking is not permitted until the date of the latest confirmed booking has passed.")
            return redirect('view_profile')

        # Create a new SilverPackage record with the form data and the current user
        silver_package = SilverPackage.objects.create(
            user=current_user,
            date_of_booking=date_of_booking,
            destination_selected=destination_selected,
            honeymoon_destination=honeymoon_destination,
            is_booked=False  # Set the initial booking status to False
        )

        # Save the SilverPackage record
        silver_package.save()

        # Redirect to a success page for a new booking
        return redirect('confirmation')

    return render(request, 'silver_booking.html')


from datetime import datetime
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import PlatinumPackage

@login_required
def platinum_booking(request):
    if request.method == 'POST':
        # Retrieve data from the form
        date_of_booking = request.POST.get('date_of_booking')
        destination_selected = request.POST.get('destination_selected')
        honeymoon_destination = request.POST.get('honeymoon_destination')

        # Get the current user (logged-in user)
        current_user = request.user

        # Check if the user already has a confirmed booking in any table
        has_confirmed_booking = (
            GoldPackage.objects.filter(user=current_user, is_booked=True).exists() or
            SilverPackage.objects.filter(user=current_user, is_booked=True).exists() or
            PlatinumPackage.objects.filter(user=current_user, is_booked=True).exists() or
            CustomisePackage.objects.filter(user=current_user, is_booked=True).exists()
        )
        
        # Retrieve the latest confirmed booking if it exists
        latest_confirmed_booking = PlatinumPackage.objects.filter(
            user=current_user, is_booked=True
        ).order_by('-date_of_booking').first()

        # Check if there is a latest confirmed booking and if its date has not passed yet
        if latest_confirmed_booking and latest_confirmed_booking.date_of_booking and latest_confirmed_booking.date_of_booking >= datetime.now().date():
            messages.error(request, f"You already have a confirmed booking. Rebooking is not permitted until the date of the latest confirmed booking has passed.")
            return redirect('view_profile')

        # Check if there is a latest confirmed booking and if its date is later than the new booking date
        if latest_confirmed_booking and latest_confirmed_booking.date_of_booking and latest_confirmed_booking.date_of_booking > datetime.strptime(date_of_booking, "%Y-%m-%d").date():
            messages.error(request, f"You already have a confirmed booking with a date later than {date_of_booking}. Rebooking is not permitted until the date of the latest confirmed booking has passed.")
            return redirect('view_profile')

        # Create a new PlatinumPackage record with the form data and the current user
        platinum_package = PlatinumPackage.objects.create(
            user=current_user,
            date_of_booking=date_of_booking,
            destination_selected=destination_selected,
            honeymoon_destination=honeymoon_destination,
            is_booked=False  # Set the initial booking status to False
        )

        # Save the PlatinumPackage record
        platinum_package.save()

        # Redirect to a success page for a new booking
        return redirect('confirmation')

    return render(request, 'platinum_booking.html')


from django.core.exceptions import ValidationError
from datetime import datetime
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import CustomisePackage

@login_required
def customise_booking(request):
    if request.method == 'POST':
        # Retrieve data from the form
        date_of_booking = request.POST.get('date_of_booking')
        destination_selected = request.POST.get('destination_selected')
        honeymoon_destination = request.POST.get('honeymoon_destination')
        hotel = request.POST.get('hotel')
        food = request.POST.get('food')
        videography = request.POST.get('videography')
        location = request.POST.get('location')
        photography = request.POST.get('photography')
        guest = request.POST.get('guest')
        billing_info_str = request.POST.get('billing_info')

        try:
            billing_info = float(billing_info_str.replace('$', ''))
        except ValueError:
            messages.error(request, "Invalid billing info. Please provide a valid numeric value.")
            return redirect('customise_booking')

        # Get the current user (logged-in user)
        current_user = request.user

        # Check if the user already has a confirmed booking in any table
        has_confirmed_booking = (
            GoldPackage.objects.filter(user=current_user, is_booked=True).exists() or
            SilverPackage.objects.filter(user=current_user, is_booked=True).exists() or
            PlatinumPackage.objects.filter(user=current_user, is_booked=True).exists() or
            CustomisePackage.objects.filter(user=current_user, is_booked=True).exists()
        )
        
        # Retrieve the latest confirmed booking if it exists
        latest_confirmed_booking = CustomisePackage.objects.filter(
            user=current_user, is_booked=True
        ).order_by('-date_of_booking').first()

        # Check if there is a latest confirmed booking and if its date has not passed yet
        if latest_confirmed_booking and latest_confirmed_booking.date_of_booking and latest_confirmed_booking.date_of_booking >= datetime.now().date():
            messages.error(request, f"You already have a confirmed booking. Rebooking is not permitted until the date of the latest confirmed booking has passed.")
            return redirect('view_profile')

        # Check if there is a latest confirmed booking and if its date is later than the new booking date
        if latest_confirmed_booking and latest_confirmed_booking.date_of_booking and latest_confirmed_booking.date_of_booking > datetime.strptime(date_of_booking, "%Y-%m-%d").date():
            messages.error(request, f"You already have a confirmed booking with a date later than {date_of_booking}. Rebooking is not permitted until the date of the latest confirmed booking has passed.")
            return redirect('view_profile')

        customise_package = CustomisePackage.objects.create(
            user=current_user,
            date_of_booking=date_of_booking,
            destination_selected=destination_selected,
            honeymoon_destination=honeymoon_destination,
            hotel=hotel,
            food=food,
            videography=videography,
            location=location,
            photography=photography,
            guest=guest,
            billing_info=billing_info,
            is_booked=False  # Set the initial booking status to False
        )

        # Save the CustomisePackage record
        customise_package.save()
        return redirect('confirmation')

    return render(request, 'customise_booking.html')


@login_required
def confirmation_view(request):
    return candy.render(request, 'confirmation.html')

@login_required
def gold(request):
     goldbookings = GoldPackage.objects.all()
    
    # Render the data in an HTML template
     return render(request, 'gold.html', {'goldbookings': goldbookings})

@login_required
def silver(request):
    silverbookings = SilverPackage.objects.all()
    
    # Render the data in an HTML template
    return render(request, 'silver.html', {'silverbookings': silverbookings})

@login_required
def platinum(request):
   platinumbookings = PlatinumPackage.objects.all()
    
    # Render the data in an HTML template
   return render(request, 'platinum.html', {'platinumbookings': platinumbookings})

@login_required
def customise(request):
   customisebookings = CustomisePackage.objects.all()
    
    # Render the data in an HTML template
   return render(request, 'customise.html', {'customisebookings': customisebookings})

@login_required
def vendordetails(request):
     vendors = VendorProfile.objects.all()

     return render(request, 'vendordetails.html', {'vendors': vendors})
   
def toggle_booking_gold(request, booking_id):
    booking = get_object_or_404(GoldPackage, id=booking_id)
    booking.is_booked = not booking.is_booked  # Toggle the booking status
    booking.save()
    
    
    if booking.is_booked:  # Corrected the model
            subject = 'Gold Booking Confirmation'
            message = 'Your Gold booking has been confirmed.'
            from_email = 'achu31395@gmail.com'
            recipient_list = [booking.user.email]  # Use booking.user.email

            send_mail(subject, message, from_email, recipient_list)
            messages.success(request, f"User '{booking.user.username}' event has been booked and email has sent.")
            return redirect("gold")

    else:
            subject = 'Gold Booking Cancellation'
            message = 'Your  Gold booking has been cancelled.'
            from_email = 'achu31395@gmail.com'
            recipient_list = [booking.user.email]  # Use booking.user.email

            send_mail(subject, message, from_email, recipient_list)
            messages.success(request, f"User '{booking.user.username}' event has cancelled and an email has sent.")
            return redirect("gold")

    return JsonResponse({'is_booked': booking.is_booked})
 
def toggle_booking_silver(request, booking_id):
    booking = get_object_or_404(SilverPackage, id=booking_id)
    booking.is_booked = not booking.is_booked  # Toggle the booking status
    booking.save()
    
    # Send confirmation or cancellation email based on the new status
    if booking.is_booked:  # Corrected the model
            subject = 'Silver Booking Confirmation'
            message = 'Your Silver booking has been confirmed.'
            from_email = 'achu31395@gmail.com'
            recipient_list = [booking.user.email]  # Use booking.user.email

            send_mail(subject, message, from_email, recipient_list)
            messages.success(request, f"User '{booking.user.username}' event has been booked and email has sent.")
            return redirect("silver")

    else:
            subject = ' Silver Booking Cancellation'
            message = 'Your Silver booking has been cancelled.'
            from_email = 'achu31395@gmail.com'
            recipient_list = [booking.user.email]  # Use booking.user.email

            send_mail(subject, message, from_email, recipient_list)
            messages.success(request, f"User '{booking.user.username}' event has cancelled and an email has sent.")
            return redirect("silver")

    return JsonResponse({'is_booked': booking.is_booked})

def toggle_booking_platinum(request, booking_id):
    booking = get_object_or_404(PlatinumPackage, id=booking_id)
    booking.is_booked = not booking.is_booked  # Toggle the booking status
    booking.save()
    
    # Send confirmation or cancellation email based on the new status
    if booking.is_booked:  # Corrected the model
            subject = ' Platinum Booking Confirmation'
            message = 'Your Platinum booking has been confirmed.'
            from_email = 'achu31395@gmail.com'
            recipient_list = [booking.user.email]  # Use booking.user.email

            send_mail(subject, message, from_email, recipient_list)
            messages.success(request, f"User '{booking.user.username}' event has been booked and email has sent.")
            return redirect("platinum")

    else:
            subject = 'Platinum Booking Cancellation'
            message = 'Your Platinum booking has been cancelled.'
            from_email = 'achu31395@gmail.com'
            recipient_list = [booking.user.email]  # Use booking.user.email

            send_mail(subject, message, from_email, recipient_list)
            messages.success(request, f"User '{booking.user.username}' event has cancelled and an email has sent.")
            return redirect("platinum")

    return JsonResponse({'is_booked': booking.is_booked})


def toggle_booking_customise(request, booking_id):
    booking = get_object_or_404(CustomisePackage, id=booking_id)
    booking.is_booked = not booking.is_booked  # Toggle the booking status
    booking.save()
    
    # Send confirmation or cancellation email based on the new status
    if booking.is_booked:  # Corrected the model
            subject = ' Customised Package Booking Confirmation'
            message = 'Your Customised booking has been confirmed.'
            from_email = 'achu31395@gmail.com'
            recipient_list = [booking.user.email]  # Use booking.user.email

            send_mail(subject, message, from_email, recipient_list)
            messages.success(request, f"User '{booking.user.username}' event has been booked and email has sent.")
            return redirect("customise")

    else:
            subject = 'Customised Package Booking Cancellation'
            message = 'Your Customised booking has been cancelled.'
            from_email = 'achu31395@gmail.com'
            recipient_list = [booking.user.email]  # Use booking.user.email

            send_mail(subject, message, from_email, recipient_list)
            messages.success(request, f"User '{booking.user.username}' event has cancelled and an email has sent.")
            return redirect("customise")

    return JsonResponse({'is_booked': booking.is_booked})

@login_required
def view_profile(request):
    user = request.user  # Get the currently logged-in user
    gold_packages = GoldPackage.objects.filter(user=user)
    silver_packages = SilverPackage.objects.filter(user=user)
    platinum_packages = PlatinumPackage.objects.filter(user=user)
    customise_packages=CustomisePackage.objects.filter(user=user)
    
    return render(request, 'view_profile.html', {
         'user':user,
        'gold_packages': gold_packages,
        'silver_packages': silver_packages,
        'platinum_packages': platinum_packages,
        'customise_packages':customise_packages
    })




@login_required
def cancel_package_gold(request, package_id):
    current_user = request.user

    # Retrieve the package based on the package_id
    try:
        gold_package = GoldPackage.objects.get(id=package_id, user=current_user)

        # Check if the cancellation is allowed (up to one day before booking date)
        booking_date = gold_package.date_of_booking  # No need to call .date() here
        current_date = timezone.now().date()  # Convert to datetime.date

        if current_date < booking_date - timedelta(days=1):
            # Send an email to the admin
            send_mail(
                'Cancellation Request',
                f'{current_user.username} has requested to cancel the Gold package with ID {gold_package.id}.',
                current_user.email,
                ['achu31395@gmail.com'],  # Replace with the admin's email address
                fail_silently=False,
            )
            
            gold_package.save()
            return redirect('cancellation')
        else:
            messages.error(request, "Cancellation is allowed up to one day before the booking date.")
            return redirect('view_profile')
    except GoldPackage.DoesNotExist:
        messages.error(request, "Package not found or it's not booked.")

    # Redirect back to the user's profile page
    return redirect('view_profile')




@login_required
def cancel_package_silver(request, package_id):
    current_user = request.user

    # Retrieve the package based on the package_id
    try:
        silver_package = SilverPackage.objects.get(id=package_id, user=current_user)

        # Check if the cancellation is allowed (up to one day before booking date)
        booking_date = silver_package.date_of_booking  # No need to call .date() here
        current_date = timezone.now().date()  # Convert to datetime.date

        if current_date < booking_date - timedelta(days=1):
            # Send an email to the admin
            send_mail(
                'Cancellation Request',
                f'{current_user.username} has requested to cancel the Platinum package with ID {silver_package.id}.',
                current_user.email,
                ['achu31395@gmail.com'],  # Replace with the admin's email address
                fail_silently=False,
            )

            # Mark the package as Cancelled
            silver_package.save()
            return redirect('cancellation')
        else:
            messages.error(request, "Cancellation is allowed up to one day before the booking date.")
            return redirect('view_profile')
    except SilverPackage.DoesNotExist:
        messages.error(request, "Package not found or it's not booked.")

    # Redirect back to the user's profile page
    return redirect('view_profile')


@login_required
def cancel_package_platinum(request, package_id):
    current_user = request.user

    # Retrieve the package based on the package_id
    try:
        platinum_package = PlatinumPackage.objects.get(id=package_id, user=current_user)

        # Check if the cancellation is allowed (up to one day before booking date)
        booking_date = platinum_package.date_of_booking  # No need to call .date() here
        current_date = timezone.now().date()  # Convert to datetime.date

        if current_date < booking_date - timedelta(days=1):
            # Send an email to the admin
            send_mail(
                'Cancellation Request',
                f'{current_user.username} has requested to cancel the Platinum package with ID {platinum_package.id}.',
                current_user.email,
                ['achu31395@gmail.com'],  # Replace with the admin's email address
                fail_silently=False,
            )

            # Mark the package as Cancelled
           
            platinum_package.save()
            return redirect('cancellation')
        else:
            messages.error(request, "Cancellation is allowed up to one day before the booking date.")
            return redirect('view_profile')
    except PlatinumPackage.DoesNotExist:
        messages.error(request, "Package not found or it's not booked.")

    # Redirect back to the user's profile page
    return redirect('view_profile')


@login_required
def cancel_package_customise(request, package_id):
    current_user = request.user

    # Retrieve the package based on the package_id
    try:
        customise_package = CustomisePackage.objects.get(id=package_id, user=current_user)

        # Check if the cancellation is allowed (up to one day before booking date)
        booking_date = customise_booking.date_of_booking  # No need to call .date() here
        current_date = timezone.now().date()  # Convert to datetime.date

        if current_date < booking_date - timedelta(days=1):
            # Send an email to the admin
            send_mail(
                'Cancellation Request',
                f'{current_user.username} has requested to cancel the Customise package with ID {customise_package.id}.',
                current_user.email,
                ['achu31395@gmail.com'],  # Replace with the admin's email address
                fail_silently=False,
            )

            # Mark the package as Cancelled
            
            customise_package.save()
            return redirect('cancellation')
        else:
            messages.error(request, "Cancellation is allowed up to one day before the booking date.")
            return redirect('view_profile')
    except CustomisePackage.DoesNotExist:
        messages.error(request, "Package not found or it's not booked.")

   
    return redirect('view_profile')

def cancellation_view(request):
     return candy.render(request,"cancellation.html")

@login_required
def delete_booking_gold(request, booking_id):
    booking = get_object_or_404(GoldPackage, id=booking_id)

    if request.method == 'POST':
        booking.delete()
        messages.success(request, f'The booking for {booking.user.username} on {booking.date_of_booking} has been deleted.')
        return redirect('gold')  

    return render(request, 'delete_booking_gold.html')  # Replace with the name of your HTML template

@login_required
def delete_booking_silver(request, booking_id):
    booking = get_object_or_404(SilverPackage, id=booking_id)

    if request.method == 'POST':
        booking.delete()
        messages.success(request, f'The booking for {booking.user.username} on {booking.date_of_booking} has been deleted.')
        return redirect('silver')  

    return render(request, 'delete_booking_silver.html')

@login_required
def delete_booking_platinum(request, booking_id):
    booking = get_object_or_404(PlatinumPackage, id=booking_id)

    if request.method == 'POST':
        booking.delete()
        messages.success(request, f'The booking for {booking.user.username} on {booking.date_of_booking} has been deleted.')
        return redirect('platinum')  

    return render(request, 'delete_booking_platinum.html')

@login_required
def delete_booking_customise(request, booking_id):
    booking = get_object_or_404(CustomisePackage, id=booking_id)

    if request.method == 'POST':
        booking.delete()
        messages.success(request, f'The booking for {booking.user.username} on {booking.date_of_booking} has been deleted.')
        return redirect('customise')  

    return render(request, 'delete_booking_customise.html')

@login_required
def confirmed_gold_bookings(request):
    # Filter GoldPackage objects where is_booked is True
    confirmed_bookings = GoldPackage.objects.filter(is_booked=True)

    # Render the details in a template or handle the data as per your requirement
    context = {'confirmed_bookings': confirmed_bookings}
    return render(request, 'confirmed_gold_bookings.html', context)


@login_required
def apply_bookings_gold(request, booking_id):
    # Get the current vendor's profile
    vendor_profile = get_object_or_404(VendorProfile, user=request.user)

    # Get the GoldPackage instance
    booking = get_object_or_404(GoldPackage, pk=booking_id)

    # Check if another vendor with the same skill has already confirmed the booking
    if GoldPackage.objects.filter(applicants__skill=vendor_profile.skill, is_confirmed=True).exists():
        messages.error(request, 'Another vendor with the same skill has already confirmed this booking.')
        return redirect('confirmed_gold_bookings')

    # Check if the current vendor has already applied for the booking
    if booking.applicants.filter(id=vendor_profile.id).exists():
        messages.warning(request, 'You have already applied for this booking.')
        return redirect('confirmed_gold_bookings')

    # Compose email content
    subject = f"Request From {request.user.role} - {vendor_profile.skill}"
    message = f"Vendor ID: {vendor_profile.id}\nDate of Booking: {booking.date_of_booking}\nDestination Selected: {booking.destination_selected}\n in Gold Package"
    from_email = request.user.email
    to_email = ['achu31395@gmail.com']  # Replace with your admin's email

    try:
        # Send email
        send_mail(subject, message, from_email, to_email)

        # Save the vendor as an applicant for this booking
        booking.applicants.add(vendor_profile)
        messages.success(request, 'Application sent successfully!')

        # Create a notification for the admin
        notification_message = f"{request.user.role} has applied on {booking.date_of_booking} for {booking.destination_selected} for Gold Package "
        Notification.objects.create(user=request.user, message=notification_message)

    except Exception as e:
        messages.error(request, f'Error sending email: {e}')

    return redirect('confirmed_gold_bookings')

@login_required
def confirmed_silver_bookings(request):
    # Filter GoldPackage objects where is_booked is True
    confirmed_bookings = SilverPackage.objects.filter(is_booked=True)

    # Render the details in a template or handle the data as per your requirement
    context = {'confirmed_bookings': confirmed_bookings}
    return render(request, 'confirmed_silver_bookings.html', context)

@login_required
def apply_bookings_silver(request, booking_id):
    # Get the current vendor's profile
    vendor_profile = get_object_or_404(VendorProfile, user=request.user)

    # Get the GoldPackage instance
    booking = get_object_or_404(SilverPackage, pk=booking_id)

    # Check if another vendor with the same skill has already confirmed the booking
    if SilverPackage.objects.filter(applicants__skill=vendor_profile.skill, is_confirmed=True).exists():
        messages.error(request, 'Another vendor with the same skill has already confirmed this booking.')
        return redirect('confirmed_silver_bookings')

    # Check if the current vendor has already applied for the booking
    if booking.applicants.filter(id=vendor_profile.id).exists():
        messages.warning(request, 'You have already applied for this booking.')
        return redirect('confirmed_silver_bookings')

    # Compose email content
    subject = f"Request From {request.user.role} - {vendor_profile.skill}"
    message = f"Vendor ID: {vendor_profile.id}\nDate of Booking: {booking.date_of_booking}\nDestination Selected: {booking.destination_selected}\n in Silver Package"
    from_email = request.user.email
    to_email = ['achu31395@gmail.com']  # Replace with your admin's email

    try:
        # Send email
        send_mail(subject, message, from_email, to_email)

        # Save the vendor as an applicant for this booking
        booking.applicants.add(vendor_profile)
        messages.success(request, 'Application sent successfully!')
        notification_message = f"{request.user.role} has applied on {booking.date_of_booking} for {booking.destination_selected} for silver Package "
        Notification.objects.create(user=request.user, message=notification_message)

    except Exception as e:
        messages.error(request, f'Error sending email: {e}')

    return redirect('confirmed_silver_bookings')


login_required
def confirmed_platinum_bookings(request):
    # Filter GoldPackage objects where is_booked is True
    confirmed_bookings = PlatinumPackage.objects.filter(is_booked=True)

    # Render the details in a template or handle the data as per your requirement
    context = {'confirmed_bookings': confirmed_bookings}
    return render(request, 'confirmed_platinum_bookings.html', context)

@login_required
def apply_bookings_platinum(request, booking_id):
    # Get the current vendor's profile
    vendor_profile = get_object_or_404(VendorProfile, user=request.user)

    # Get the GoldPackage instance
    booking = get_object_or_404(PlatinumPackage, pk=booking_id)

    # Check if another vendor with the same skill has already confirmed the booking
    if PlatinumPackage.objects.filter(applicants__skill=vendor_profile.skill, is_confirmed=True).exists():
        messages.error(request, 'Another vendor with the same skill has already confirmed this booking.')
        return redirect('confirmed_platinum_bookings')

    # Check if the current vendor has already applied for the booking
    if booking.applicants.filter(id=vendor_profile.id).exists():
        messages.warning(request, 'You have already applied for this booking.')
        return redirect('confirmed_platinum_bookings')

    # Compose email content
    subject = f"Request From {request.user.role} - {vendor_profile.skill}"
    message = f"Vendor ID: {vendor_profile.id}\nDate of Booking: {booking.date_of_booking}\nDestination Selected: {booking.destination_selected}\n in Platinum Package"
    from_email = request.user.email
    to_email = ['achu31395@gmail.com']  # Replace with your admin's email

    try:
        # Send email
        send_mail(subject, message, from_email, to_email)

        # Save the vendor as an applicant for this booking
        booking.applicants.add(vendor_profile)
        messages.success(request, 'Application sent successfully!')
        notification_message = f"{request.user.role} has applied on {booking.date_of_booking} for {booking.destination_selected} for Platinum Package "
        Notification.objects.create(user=request.user, message=notification_message)

    except Exception as e:
        messages.error(request, f'Error sending email: {e}')

    return redirect('confirmed_platinum_bookings')

login_required
def confirmed_customise_bookings(request):
    # Filter GoldPackage objects where is_booked is True
    confirmed_bookings = CustomisePackage.objects.filter(is_booked=True)

    # Render the details in a template or handle the data as per your requirement
    context = {'confirmed_bookings': confirmed_bookings}
    return render(request, 'confirmed_customise_bookings.html', context)

@login_required
def apply_bookings_customise(request, booking_id):
    # Get the current vendor's profile
    vendor_profile = get_object_or_404(VendorProfile, user=request.user)

    # Get the GoldPackage instance
    booking = get_object_or_404(CustomisePackage, pk=booking_id)

    # Check if another vendor with the same skill has already confirmed the booking
    if CustomisePackage.objects.filter(applicants__skill=vendor_profile.skill, is_confirmed=True).exists():
        messages.error(request, 'Another vendor with the same skill has already confirmed this booking.')
        return redirect('confirmed_customise_bookings')

    # Check if the current vendor has already applied for the booking
    if booking.applicants.filter(id=vendor_profile.id).exists():
        messages.warning(request, 'You have already applied for this booking.')
        return redirect('confirmed_customise_bookings')

    # Compose email content
    subject = f"Request From {request.user.role} - {vendor_profile.skill}"
    message = f"Vendor ID: {vendor_profile.id}\nDate of Booking: {booking.date_of_booking}\nDestination Selected: {booking.destination_selected}\n in Gold Package"
    from_email = request.user.email
    to_email = ['achu31395@gmail.com']  # Replace with your admin's email

    try:
        # Send email
        send_mail(subject, message, from_email, to_email)

        # Save the vendor as an applicant for this booking
        booking.applicants.add(vendor_profile)
        messages.success(request, 'Application sent successfully!')
        notification_message = f"{request.user.role} has applied on {booking.date_of_booking} for {booking.destination_selected} for Customise Package "
        Notification.objects.create(user=request.user, message=notification_message)

    except Exception as e:
        messages.error(request, f'Error sending email: {e}')

    return redirect('confirmed_customise_bookings')


def vendorpackageapply(request):
    gold_bookings = GoldPackage.objects.filter(is_booked=True)
    silver_bookings = SilverPackage.objects.filter(is_booked=True)
    platinum_bookings = PlatinumPackage.objects.filter(is_booked=True)
    customise_bookings = CustomisePackage.objects.filter(is_booked=True)

    # Get all registered vendors
    vendors = VendorProfile.objects.all()

    context = {
        'gold_bookings': gold_bookings,
        'silver_bookings': silver_bookings,
        'platinum_bookings': platinum_bookings,
        'customise_bookings': customise_bookings,
        'vendors': vendors,
    }

    return render(request, 'vendorpackageapply.html', context)



from django.shortcuts import get_object_or_404, redirect

def confirm_booking_gold_vendor(request, booking_id):
    # Get the GoldPackage instance
    gold_booking = get_object_or_404(GoldPackage, id=booking_id)

    # Assuming there's a ForeignKey from GoldPackage to User
    vendor_user = gold_booking.user

    # Admin's email
    admin_email = 'achu31395@gmail.com'  # Replace with your admin's email

    # Vendor's email
    vendor_email = vendor_user.email  # Access the related User's email directly

    # Send email
    send_mail(
        'Booking Confirmation',
        'Dear Vendor, Your booking has been confirmed for the Gold Package.',
        admin_email,  # From email address (admin's email)
        [vendor_email],  # To email address (vendor's email)
        fail_silently=False,
    )

    # Perform other actions related to confirmation here, e.g., updating the booking status
    gold_booking.is_confirmed = True
    gold_booking.save()

    return redirect('vendorpackageapply')


    return render(request,"confirm_booking_gold_vendor.html")



from django.shortcuts import get_object_or_404, redirect

def confirm_booking_silver_vendor(request, booking_id):
    # Get the GoldPackage instance
    silver_booking = get_object_or_404(SilverPackage, id=booking_id)

    # Assuming there's a ForeignKey from GoldPackage to User
    vendor_user = silver_booking.user

    # Admin's email
    admin_email = 'achu31395@gmail.com'  # Replace with your admin's email

    # Vendor's email
    vendor_email = vendor_user.email  # Access the related User's email directly

    # Send email
    send_mail(
        'Booking Confirmation',
        'Dear Vendor, Your booking has been confirmed for the Silver Package.',
        admin_email,  # From email address (admin's email)
        [vendor_email],  # To email address (vendor's email)
        fail_silently=False,
    )

    # Perform other actions related to confirmation here, e.g., updating the booking status
    silver_booking.is_confirmed = True
    silver_booking.save()

    return redirect('vendorpackageapply')


    return render(request,"confirm_booking_silver_vendor.html")



from django.shortcuts import get_object_or_404, redirect

def confirm_booking_platinum_vendor(request, booking_id):
    # Get the GoldPackage instance
    platinum_booking = get_object_or_404(PlatinumPackage, id=booking_id)

    # Assuming there's a ForeignKey from GoldPackage to User
    vendor_user = platinum_booking.user

    # Admin's email
    admin_email = 'achu31395@gmail.com'  # Replace with your admin's email

    # Vendor's email
    vendor_email = vendor_user.email  # Access the related User's email directly

    # Send email
    send_mail(
        'Booking Confirmation',
        'Dear Vendor, Your booking has been confirmed for the Platinum Package.',
        admin_email,  # From email address (admin's email)
        [vendor_email],  # To email address (vendor's email)
        fail_silently=False,
    )

    # Perform other actions related to confirmation here, e.g., updating the booking status
    platinum_booking.is_confirmed = True
    platinum_booking.save()

    return redirect('vendorpackageapply')


    return render(request,"confirm_booking_platinum_vendor.html")


from django.shortcuts import get_object_or_404, redirect

def confirm_booking_customise_vendor(request, booking_id):
    # Get the GoldPackage instance
    customise_booking = get_object_or_404(CustomisePackage, id=booking_id)

    # Assuming there's a ForeignKey from GoldPackage to User
    vendor_user = customise_booking.user

    # Admin's email
    admin_email = 'achu31395@gmail.com'  # Replace with your admin's email

    # Vendor's email
    vendor_email = vendor_user.email  # Access the related User's email directly

    # Send email
    send_mail(
        'Booking Confirmation',
        'Dear Vendor, Your booking has been confirmed for the Customise Package.',
        admin_email,  # From email address (admin's email)
        [vendor_email],  # To email address (vendor's email)
        fail_silently=False,
    )

    # Perform other actions related to confirmation here, e.g., updating the booking status
    customise_booking.is_confirmed = True
    customise_booking.save()

    return redirect('vendorpackageapply')


    return render(request,"confirm_booking_customise_vendor.html")

@login_required
def payments(request):
    user = request.user  # Get the currently logged-in user
    gold_packages = GoldPackage.objects.filter(user=user)
    silver_packages = SilverPackage.objects.filter(user=user)
    platinum_packages = PlatinumPackage.objects.filter(user=user)
    customise_packages=CustomisePackage.objects.filter(user=user)
    
    return render(request, 'payments.html', {
         'user':user,
        'gold_packages': gold_packages,
        'silver_packages': silver_packages,
        'platinum_packages': platinum_packages,
        'customise_packages':customise_packages
    })

import razorpay
@login_required
def payment_gold(request):
  if request.method== 'POST' :  
    client = razorpay.Client(auth=("rzp_test_XxJHDi3GQ6Raye", "ETHQMabGv3tFBgWHtt6cGCf9"))

    DATA = {
        "amount": 100,
        "currency": "INR",
    }
    client.order.create({'amount':'amount','currency':'INR','payment_cpature':'1'})
  return render(request,"payment_gold.html")

@login_required
def payment_silver(request):
    return render(request,"payment_silver.html")

@login_required
def payment_platinum(request):
    return render(request,"payment_platinum.html")

@login_required
def payment_customise(request):
    return render(request,"payment_customise.html")

# weather prediction
from django.conf import settings
import requests
from datetime import datetime
@login_required
def predict_weather(request):
    if request.method == 'POST':
        location = request.POST.get('location')
        date = request.POST.get('date')
        
        api_key = settings.OPENWEATHERMAP_API_KEY
        base_url = 'http://api.openweathermap.org/data/2.5/weather'
        params = {
            'q': location,
            'appid': api_key,
        }

        response = requests.get(base_url, params=params)
        data = response.json()

        if data['cod'] == '404':
            messages.error(request,"Enter valid city")
            return redirect('predict_weather')

        context = {
            'location': location,
            'date': datetime.strptime(date, '%Y-%m-%d').date(),
            'temperature': data['main']['temp'],
            'weather_description': data['weather'][0]['description'],
        }

        return render(request, 'weather_prediction.html', context)

    return render(request, 'weather_prediction_form.html')

from weddingapp.models import Thread
@login_required
def messages_page(request):
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
    context = {
        'Threads': threads
    }
    return render(request, 'messages.html', context)


import PyPDF2
def verify_keywords_in_document(pdf_path):
    # Define the keywords to be verified
    keywords_to_verify = ["Nam e", "Gender", "Skill", "Mobile Number", "Date of Birth", "Document Number", "Work Experience", "Country"]

    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)

            # Iterate through each page in the PDF
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                # print(f"Page {page_num + 1}:\n{text}\n{'-'*50}\n")
                
                # Check if any keyword is missing in the text
                if any(keyword not in text for keyword in keywords_to_verify):
                    return False

            # All keywords found on all pages
            return True

    except Exception as e:
        print(f"Error during PDF verification: {e}")

    return False

def verify_document(request, vendor_id):
    # Retrieve the vendor object based on the vendor_id
    vendor = get_object_or_404(VendorProfile, id=vendor_id)

    # Perform document verification logic here
    verification_result = verify_keywords_in_document(vendor.document.path)

    # Update the verification status in the user profile
    vendor.user.is_verified = verification_result
    vendor.user.save()

    # Return a JSON response indicating the result
    return JsonResponse({'success': verification_result})




from .models import Review
from textblob import TextBlob

def review_form(request):
    review=Review.objects.all()
    if request.method == 'POST':
        review_text = request.POST.get('review_text', '')
        if review_text:
            # Calculate sentiment rating using TextBlob
            blob = TextBlob(review_text)
            sentiment_rating = blob.sentiment.polarity
            # Save review to the database
            Review.objects.create(reviewer=request.user, review_text=review_text, sentiment_rating=sentiment_rating)
            return redirect('review_form')  # Redirect to the same page after submitting
    return render(request, 'review_form.html',{'review':review})




def get_location_suggestions(request):
    query = request.GET.get('query', '')  # Get the query string from the request
    api_key = 'a15a0ad853484a0b8957d2832012fb69'  # Replace 'your_api_key' with your actual Geoapify API key
    api_url = f'https://api.geoapify.com/v1/geocode/autocomplete?text={query}&apiKey={api_key}'
    

    
    # Fetch location suggestions from the Geoapify API
    response = requests.get(api_url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        suggestions = response.json()  # Parse the JSON response
        return JsonResponse(suggestions, safe=False)  # Return the suggestions as JSON response
    else:
        # If there was an error fetching suggestions, return an error response
        return JsonResponse({'error': 'Failed to fetch suggestions'}, status=500)




def keralaview(request):
    return render(request, 'keralaview.html')

def delhiview(request):
    return render(request, 'delhiview.html')

def rajview(request):
    return render(request, 'rajview.html')

def parisview(request):
    return render(request, 'parisview.html')  

def luxview(request):
    return render(request, 'luxview.html')  

def swizview(request):
    return render(request, 'swizview.html')