from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, EnquiryForm, BudgetPlannerForm, TravelBuddyForm, TravelCostForm,CurrencyConverterForm,BlogForm,OTPForm
from .models import TravelBuddy, TravelGoal,Destination, Enquiry, BudgetPlanner, Package, Destination, Blog,CurrencyConverter,Blog,EmailOTP
from django.contrib.auth.models import User
from django.contrib import messages
import random
from django.core.mail import send_mail
from django.conf import settings

def home(request):

    return render(request, 'home.html')

def about(request):

    return render(request, 'about.html')

def contact(request):

    return render(request, 'contact.html')

def packages(request):

    india = Destination.objects.filter(package__category='India')

    international = Destination.objects.filter(package__category='International')

    europe = Destination.objects.filter(package__category='Europe')

    honeymoon = Destination.objects.filter(package__category='Honeymoon')

    context = {

        'india': india,

        'international': international,

        'europe': europe,

        'honeymoon': honeymoon,

    }

    return render(request, 'packages.html', context)

def destinations(request, category):

    package = Package.objects.get(category=category)

    destinations = Destination.objects.filter(package=package)

    sort = request.GET.get("sort")

    if sort == "price_low":
        destinations = destinations.order_by("price")

    elif sort == "price_high":
        destinations = destinations.order_by("-price")

    elif sort == "rating":
        destinations = destinations.order_by("-rating")

    elif sort == "days_low":
        destinations = destinations.order_by("days")

    elif sort == "days_high":
        destinations = destinations.order_by("-days")

    elif sort == "name":
        destinations = destinations.order_by("destination_name")

    context = {

        "package": package,

        "destinations": destinations,

        "sort": sort,

    }

    return render(request, "destinations.html", context)

@login_required
def blog(request):

    if request.method == "POST":

        form = BlogForm(request.POST, request.FILES)

        if form.is_valid():

            blogs = form.save(commit=False)

            blogs.user = request.user

            blogs.save()

            return redirect('blog')

    else:

        form = BlogForm()

    blogs = Blog.objects.all().order_by('-created_at')

    context = {

        "form": form,

        "blogs": blogs,

    }

    return render(request, "blog.html", context)

def signup(request):

    if request.method == "POST":

        form = SignupForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data["username"]

            email = form.cleaned_data["email"]

            password = form.cleaned_data["password"]

            confirm_password = form.cleaned_data["confirm_password"]

            if password != confirm_password:

                messages.error(request, "Passwords do not match.")

            elif User.objects.filter(username=username).exists():

                messages.error(request, "Username already exists.")

            else:

                user = User.objects.create_user(

                    username=username,

                    email=email,

                    password=password,

                    is_active=False

                )

                otp = str(random.randint(100000, 999999))

                EmailOTP.objects.create(

                    user=user,

                    otp=otp

                )

                send_mail(

                    "JourneyMap Email Verification",

                    f"Your OTP is: {otp}",

                    settings.EMAIL_HOST_USER,

                    [email],

                    fail_silently=False,

                )

                request.session["user_id"] = user.id

                return redirect("verify_otp")

    else:

        form = SignupForm()

    return render(request, "signup.html", {"form": form})

def user_login(request):

    if request.method == "POST":

        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():

            login(request, form.get_user())

            return redirect('home')

    else:

        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def user_logout(request):

    logout(request)

    return redirect('home')

@login_required
def enquiry(request, destination_id):

    destination = Destination.objects.get(id=destination_id)

    if request.method == "POST":

        form = EnquiryForm(request.POST)

        if form.is_valid():

            enquiry = form.save(commit=False)

            enquiry.user = request.user

            enquiry.destination = destination

            enquiry.status = "Pending"

            enquiry.save()

            return redirect("home")

    else:

        form = EnquiryForm()

    context = {
        
        "form": form,
        
        "destination": destination,
        
    }

    return render(request, "enquiry.html", context)
    
@login_required
def travel_goal(request):

    completed_trips = Enquiry.objects.filter(
        
        user=request.user,
        
        status="Completed",
        
        destination__package__category__in=[
            
            "International",
            
            "Europe",
            
            "Honeymoon",
            
        ]
    )

    completed_count = completed_trips.count()

    if completed_count >= 2:
        
        progress = 100
        
    elif completed_count == 1:
        
        progress = 50
        
    else:
        
        progress = 0

    reward = completed_count >= 2

    context = {
        
        "completed_trips": completed_trips,
        
        "completed_count": completed_count,
        
        "progress": progress,
        
        "reward": reward,
        
    }

    return render(request, "travel_goal.html", context)

@login_required
def budget_planner(request):

    remaining = None
    
    affordable_packages = []

    if request.method == "POST":

        total_budget = int(request.POST.get("total_budget"))
        
        transport = int(request.POST.get("transport"))
        
        hotel = int(request.POST.get("hotel"))
        
        food = int(request.POST.get("food"))
        
        shopping = int(request.POST.get("shopping"))

        total_expense = transport + hotel + food + shopping

        remaining = total_budget - total_expense

        affordable_packages = Package.objects.filter(price__lte=remaining)

    context = {

        "remaining": remaining,
        
        "packages": affordable_packages,

    }

    return render(request, "budget_planner.html", context)

@login_required
def travel_cost(request):

    total_cost = None

    if request.method == "POST":

        form = TravelCostForm(request.POST)

        if form.is_valid():

            travel = form.save(commit=False)

            travel.user = request.user

            destination_price = travel.destination.price

            if travel.hotel_type == "Standard":

                hotel_price = 1000

            elif travel.hotel_type == "Deluxe":

                hotel_price = 2500

            else:

                hotel_price = 5000

            total_cost = (destination_price * travel.people) + (hotel_price * travel.days)

            travel.estimated_cost = total_cost

            travel.save()

    else:

        form = TravelCostForm()

    context = {

        'form': form,

        'total_cost': total_cost,

    }

    return render(request,'travel_cost.html',context)
    
@login_required
def travel_buddy(request):

    buddies = None

    if request.method == "POST":

        form = TravelBuddyForm(request.POST)

        if form.is_valid():

            buddy = form.save(commit=False)

            buddy.user = request.user

            buddy.save()

            buddies = TravelBuddy.objects.filter(

                destination=buddy.destination,

                interest=buddy.interest

            ).exclude(user=request.user)

    else:

        form = TravelBuddyForm()

    context = {

        "form": form,

        "buddies": buddies,

    }

    return render(request,"travel_buddy.html",context)
    
@login_required
def currency_converter(request):

    converted_amount = None

    to_currency = None

    if request.method == "POST":

        form = CurrencyConverterForm(request.POST)

        if form.is_valid():

            currency = form.save(commit=False)

            currency.user = request.user

            amount = currency.amount

            from_currency = currency.from_currency

            to_currency = currency.to_currency

            rates = {

                "INR": 1,

                "USD": 0.0105,

                "EUR": 0.0090,

                "GBP": 0.0077,

                "AED": 0.0386,

                "JPY": 1.55,

                "SGD": 0.0135,

                "CAD": 0.0144,

            }

            inr_amount = amount / rates[from_currency]

            converted_amount = inr_amount * rates[to_currency]

            converted_amount = round(converted_amount, 2)

            currency.converted_amount = converted_amount

            currency.save()

    else:

        form = CurrencyConverterForm()

    context = {

        "form": form,

        "converted_amount": converted_amount,

        "to_currency": to_currency,

    }

    return render(request,"currency_converter.html",context)

def verify_otp(request):

    user_id = request.session.get("user_id")

    if not user_id:

        return redirect("signup")

    user = User.objects.get(id=user_id)

    otp_data = EmailOTP.objects.get(user=user)

    if request.method == "POST":

        form = OTPForm(request.POST)

        if form.is_valid():

            entered_otp = form.cleaned_data["otp"]

            if entered_otp == otp_data.otp:

                otp_data.is_verified = True

                otp_data.save()

                user.is_active = True

                user.save()

                messages.success(request, "Email verified successfully.")

                return redirect("login")

            else:

                messages.error(request, "Invalid OTP")

    else:

        form = OTPForm()

    context = {

        "form": form,

        "email": user.email,

    }

    return render(request, "verify_otp.html", context)