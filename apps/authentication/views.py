from django.shortcuts import render, redirect
from .models import User,OTP
from django.contrib.auth import authenticate, login
import random
from django.core.mail import send_mail
from django.conf import settings


def signup(request):

    if request.method == 'POST':

        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        referral = request.POST.get('referral')

        # password match validation
        if password != confirm_password:
            return render(request, 'signup.html', {
                'error': 'Passwords do not match'
            })

        # email already exists
        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {
                'error': 'Email already exists'
            })
        #mobile number validation
        if User.objects.filter(mobile_number=mobile_number).exists():
            return render(request, 'signup.html', {
                'error': 'Mobile number already exists'
            })

        # create user
        user = User.objects.create_user(
            username=email,
            full_name=full_name,
            email=email,
            mobile_number=mobile_number,
            password=password,
            referral_code=referral
        )

        return redirect('login')

    return render(request, 'signup.html')


def login_view(request):

    if request.method == 'POST':

        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('home')

        else:

            return render(request, 'login.html', {
                'error': 'Invalid email or password'
            })

    return render(request, 'login.html')

def home(request):

    return render(request, 'home.html')

def forgot_password(request):

    if request.method == 'POST':

        email = request.POST.get('email')

        try:

            user = User.objects.get(email=email)

            otp = str(random.randint(100000, 999999))

            OTP.objects.create(
                user=user,
                otp_code=otp
            )

            send_mail(
                'Scentora Password Reset OTP',
                f'Your OTP is {otp}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            request.session['reset_email'] = email

            return redirect('verify_otp')

        except User.DoesNotExist:

            print('User does not exist')

    return render(
        request,
        'forgot_password.html'
    )

def verify_otp(request):
    return render(request, 'verify_otp.html')