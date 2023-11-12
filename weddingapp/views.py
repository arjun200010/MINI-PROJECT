from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth import logout
from django.contrib import messages
from django.urls import reverse
from .models import User,UserProfile,VendorProfile
from .models import GoldPackage,SilverPackage,PlatinumPackage,CustomisePackage
from django.contrib.auth.decorators import login_required
import json
from django.shortcuts import get_object_or_404, redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model

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

    return render(request, 'signup.html')

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
                return redirect("vendor_update_profile")
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

        context = {
            'user_count': user_count,
            'vendor_count': vendor_count,
            'active_booking_count': active_booking_count,
        }

        response = render(request, 'adminfirst.html', context)
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




# views.py




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

        # Update VendorProfile fields
        vendor_profile.skill = skill
        vendor_profile.document = document
        vendor_profile.save()

        # Update UserProfile fields
        user = get_object_or_404(User, pk=request.user.id)
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()

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
            CustomisePackage.objects.filter(user=current_user,is_booked=True).exists()
        )
        # Create a new GoldPackage record with the form data and the current user
        gold_package = GoldPackage.objects.create(
            user=current_user,
            date_of_booking=date_of_booking,
            destination_selected=destination_selected,
            is_booked=False  # Set the initial booking status to False
        )

        # Save the GoldPackage record
        gold_package.save()

        # If the user has a confirmed booking, redirect to a different page
        if has_confirmed_booking:
            messages.error(request,"You already has a confirm booking and REBOOKING IS NOT PERMITTED")
            return redirect('view_profile')
        else:
            # Redirect to a success page for a new booking
            return redirect('confirmation')

    return render(request, 'gold_booking.html')



@login_required
def silver_booking(request):
    if request.method == 'POST':
        # Retrieve data from the form
        date_of_booking = request.POST.get('date_of_booking')
        destination_selected = request.POST.get('destination_selected')
        honeymoon_destination=request.POST.get('honeymoon_destination')

        # Get the current user (logged-in user)
        current_user = request.user

        # Check if the user already has a confirmed booking in any table
        has_confirmed_booking = (
            GoldPackage.objects.filter(user=current_user, is_booked=True).exists() or
            SilverPackage.objects.filter(user=current_user, is_booked=True).exists() or
            PlatinumPackage.objects.filter(user=current_user, is_booked=True).exists() or
            CustomisePackage.objects.filter(user=current_user,is_booked=True).exists()
        )
        # Create a new GoldPackage record with the form data and the current user
        silver_package = SilverPackage.objects.create(
            user=current_user,
            date_of_booking=date_of_booking,
            destination_selected=destination_selected,
            honeymoon_destination=honeymoon_destination,
            is_booked=False  # Set the initial booking status to False
        )

        # Save the GoldPackage record
        silver_package.save()

        # If the user has a confirmed booking, redirect to a different page
        if has_confirmed_booking:
            messages.error(request,"You already has a confirm booking and REBOOKING IS NOT PERMITTED")
            return redirect('view_profile')
        else:
            # Redirect to a success page for a new booking
            return redirect('confirmation')

    return render(request, 'silver_booking.html')

@login_required
def platinum_booking(request):
    if request.method == 'POST':
        # Retrieve data from the form
        date_of_booking = request.POST.get('date_of_booking')
        destination_selected = request.POST.get('destination_selected')
        honeymoon_destination=request.POST.get('honeymoon_destination')

        # Get the current user (logged-in user)
        current_user = request.user

        # Check if the user already has a confirmed booking in any table
        has_confirmed_booking = (
            GoldPackage.objects.filter(user=current_user, is_booked=True).exists() or
            SilverPackage.objects.filter(user=current_user, is_booked=True).exists() or
            PlatinumPackage.objects.filter(user=current_user, is_booked=True).exists() or
            CustomisePackage.objects.filter(user=current_user,is_booked=True).exists()
        )
        # Create a new GoldPackage record with the form data and the current user
        platinum_package = PlatinumPackage.objects.create(
            user=current_user,
            date_of_booking=date_of_booking,
            destination_selected=destination_selected,
            honeymoon_destination=honeymoon_destination,
            is_booked=False  # Set the initial booking status to False
        )

        # Save the GoldPackage record
        platinum_package.save()

        # If the user has a confirmed booking, redirect to a different page
        if has_confirmed_booking:
            messages.error(request,"You already has a confirm booking and REBOOKING IS NOT PERMITTED")
            return redirect('view_profile')
        else:
            # Redirect to a success page for a new booking
            return redirect('confirmation')

    return render(request, 'platinum_booking.html')

from django.core.exceptions import ValidationError

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

        # Create a new CustomisePackage record with the form data and the current user
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

        # If the user has a confirmed booking, redirect to a different page
        if has_confirmed_booking:
            messages.error(request, "You already have a confirmed booking, and REBOOKING IS NOT PERMITTED.")
            return redirect('view_profile')
        else:
            # Redirect to a success page for a new booking
            return redirect('confirmation')

    return render(request, 'customise_booking.html')

@login_required
def confirmation_view(request):
    return render(request, 'confirmation.html')

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
        gold_package = GoldPackage.objects.get(id=package_id, user=current_user, is_booked=False)
        # Send an email to the admin
        send_mail(
            'Cancellation Request',
            f'{current_user.username} has requested to cancel the Gold package with ID {gold_package.id}.',
            current_user.email,
            ['achu31395@gmail.com'],  # Replace with the admin's email address
            fail_silently=False,
        )
        # Mark the package as Cancelled
        gold_package.is_booked = False
        gold_package.save()
        return redirect('cancellation')
    except GoldPackage.DoesNotExist:
        messages.error(request, "Package not found or it's already cancelled.")

    # Redirect back to the user's profile page
    return redirect('view_profile')

@login_required
def cancel_package_silver(request, package_id):
    current_user = request.user

    # Retrieve the package based on the package_id
    try:
        silver_package = SilverPackage.objects.get(id=package_id, user=current_user, is_booked=False)
        # Send an email to the admin
        send_mail(
            'Cancellation Request',
            f'{current_user.username} has requested to cancel the Gold package with ID {silver_package.id}.',
            current_user.email,
            ['achu31395@gmail.com'],  # Replace with the admin's email address
            fail_silently=False,
        )
        # Mark the package as Cancelled
        silver_package.is_booked = False
        silver_package.save()
        return redirect('cancellation')
    except SilverPackage.DoesNotExist:
        messages.error(request, "Package not found or it's already cancelled.")

    # Redirect back to the user's profile page
    return redirect('view_profile')

@login_required
def cancel_package_platinum(request, package_id):
    current_user = request.user

    # Retrieve the package based on the package_id
    try:
        platinum_package = PlatinumPackage.objects.get(id=package_id, user=current_user, is_booked=False)
        # Send an email to the admin
        send_mail(
            'Cancellation Request',
            f'{current_user.username} has requested to cancel the Gold package with ID {platinum_package.id}.',
            current_user.email,
            ['achu31395@gmail.com'],  # Replace with the admin's email address
            fail_silently=False,
        )
        # Mark the package as Cancelled
        platinum_package.is_booked = False
        platinum_package.save()
        return redirect('cancellation')
    except PlatinumPackage.DoesNotExist:
        messages.error(request, "Package not found or it's already cancelled.")

    # Redirect back to the user's profile page
    return redirect('view_profile')

@login_required
def cancel_package_customise(request, package_id):
    current_user = request.user

    # Retrieve the package based on the package_id
    try:
        customise_package = CustomisePackage.objects.get(id=package_id, user=current_user, is_booked=False)
        # Send an email to the admin
        send_mail(
            'Cancellation Request',
            f'{current_user.username} has requested to cancel the Customise package with ID {customise_package.id}.',
            current_user.email,
            ['achu31395@gmail.com'],  # Replace with the admin's email address
            fail_silently=False,
        )
        # Mark the package as Cancelled
        customise_package.is_booked = False
        customise_package.save()
        return redirect('cancellation')
    except PlatinumPackage.DoesNotExist:
        messages.error(request, "Package not found or it's already cancelled.")

    # Redirect back to the user's profile page
    return redirect('view_profile')


def cancellation_view(request):
     return render(request,"cancellation.html")




