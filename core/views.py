
from django.http import JsonResponse
import subprocess
import sys
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
from .forms import SignUpForm, LoginForm, ProfileForm, TradeForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile, PerformanceMetrics, Trade
from core.models import CustomUser
from api.crypto import get_crypto_prices, get_crypto_news
from api.calculations import update_performance_metrics
import requests
from django.contrib.auth.decorators import login_required

@login_required
def base(request):
    profile = Profile.objects.filter(user=request.user).first()
    if not profile:
        return redirect('profile')  # Redirect to profile setup if incomplete
    
    metrics = PerformanceMetrics.objects.filter(user=request.user).first()
    trades = Trade.objects.filter(user=request.user).order_by('-trade_time')
    live_prices = get_crypto_prices()  # Correct function name
    print("Live Prices:", live_prices)
    news = get_crypto_news("bitcoin")  # Provide a coin name as argument
    print("News:", news)

    return render(request, 'base.html', {
        'profile': profile,
        'metrics': metrics,
        'trades': trades,
        'live_prices': live_prices,
        'news': news,
    })

# Get live cryptocurrency prices
from django.http import JsonResponse
from api.crypto import get_crypto_prices, get_crypto_news
from api.calculations import calculate_total_return, calculate_max_drawdown

# View for getting crypto prices
def crypto_prices_view(request):
    prices = get_crypto_prices()
    if prices:
        return JsonResponse(prices)
    return JsonResponse({"error": "Unable to fetch prices"}, status=500)

# View for getting crypto news
def crypto_news_view(request, coin_name):
    news = get_crypto_news(coin_name)
    return JsonResponse(news, safe=False)

# View for calculating metrics
def calculate_metrics_view(request):
    trades = [{"balance": 1000}, {"balance": 1100}, {"balance": 950}]
    metrics = {
        "total_return": calculate_total_return(trades),
        "max_drawdown": calculate_max_drawdown(trades),
    }
    return JsonResponse(metrics)

@login_required
def strategyoverview(request):
    return render(request, "strategyoverview.html")
  
@login_required
def tradeslog(request):
    return render(request, "tradeslog.html")

@login_required
def performanceanalytics(request):
    return render(request, "performanceanalytics.html")

@login_required
def performance_chart(request):
    return render(request, 'performance_chart.html')
# def performance_chart(request):
#     return render(request, 'performance_chart.html')
@login_required
def ent_details(request):
    return render(request, "payment_details.html") 
@login_required
def start_streamlit(request):
    """Start the Streamlit environment."""
    try:
        subprocess.Popen([sys.executable, "E:/TRDAlgo/Django_streamliyProject/backtesting/run.py"])
        return JsonResponse({"message": "Streamlit environment is starting. Please wait..."})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
#-coins functions
def news_bitcoin(request):
    articles = [
        {"title": "Bitcoin hits new high", "content": "Bitcoin price reaches a new all-time high.", "date": "2025-01-01"},
        {"title": "Bitcoin adoption increases", "content": "More companies are adopting Bitcoin as a payment method.", "date": "2025-01-02"},
        # Add more articles as needed
    ]
    return render(request, 'news.html', {'coin_name': 'Bitcoin', 'articles': articles})

def news_ethereum(request):
    articles = [
        {"title": "Ethereum 2.0 launch", "content": "Ethereum 2.0 is set to launch soon.", "date": "2025-01-01"},
        {"title": "Ethereum price surge", "content": "Ethereum price surges due to increased demand.", "date": "2025-01-02"},
        # Add more articles as needed
    ]
    return render(request, 'news.html', {'coin_name': 'Ethereum', 'articles': articles})

def news_ripple(request):
    articles = [
        {"title": "Ripple partners with major bank", "content": "Ripple announces a new partnership with a major bank.", "date": "2025-01-01"},
        {"title": "Ripple price analysis", "content": "An in-depth analysis of Ripple's recent price movements.", "date": "2025-01-02"},
        # Add more articles as needed
    ]
    return render(request, 'news.html', {'coin_name': 'Ripple', 'articles': articles})

def news_litecoin(request):
    articles = [
        {"title": "Litecoin halving reached event", "content": "Litecoin's halving event is approaching.", "date": "2025-01-01"},
        {"title": "Litecoin price prediction", "content": "Experts predict Litecoin's price for the next year.", "date": "2025-01-02"},
        # Add more articles as needed
    ]
    return render(request, 'news.html', {'coin_name': 'Litecoin', 'articles': articles})

def news_cardano(request):
    articles = [
        {"title": "Cardano smart contracts", "content": "Cardano introduces new smart contract features.", "date": "2025-01-01"},
        {"title": "Cardano price rally", "content": "Cardano's price rallies due to positive news.", "date": "2025-01-02"},
        # Add more articles as needed
    ]
    return render(request, 'news.html', {'coin_name': 'Cardano', 'articles': articles})


def signup_view(request):
    if request.method == 'POST':
        # Extract form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if passwords match
        if password != confirm_password:
            return render(request, 'registration/signup.html', {'error': 'Passwords do not match'})

        try:
            # Create a new user (ensure CustomUser model is used if you have one)
            user = User.objects.create_user(username=name, email=email, password=password)
            user.save()

            # Log the user in after successful signup
            login(request, user)

            # Redirect to the profile page
            return redirect('profile')  # Ensure 'profile' is a valid URL name
        except Exception as e:
            # Handle exceptions (e.g., duplicate username, validation errors)
            return render(request, 'registration/signup.html', {'error': str(e)})
    
    # Render the signup page for GET requests
    return render(request, 'registration/signup.html')

#_ login view -------------------------------
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()  # Get authenticated user
            login(request, user)  # Log the user in
            return redirect('base')  # Redirect to the dashboard or another existing view
    else:
        form = AuthenticationForm()  # Empty form for GET request
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')
User = get_user_model()
def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

def landingpage(request):
    return render(request, "landingpage.html")

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm

# @login_required
# def profile_view(request):
#     # Get or create a profile for the logged-in user
#     profile, created = Profile.objects.get_or_create(user=request.user)

#     if request.method == 'POST':
#         form = ProfileForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()  # Save the profile instance
#             return render(request, 'profile/profile.html', {'form': form, 'success': True})  # Pass 'success' to indicate it's successful submission 
#     else:
#         form = ProfileForm(instance=profile)

#     return render(request, 'profile/profile.html', {'form': form, 'success': False})

@login_required
def profile_view(request):
    print("profile view called")
    profile, created = Profile.objects.get_or_create(user=request.user)
    print("profile is created:", profile, created)  # Debug print statement

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            print("form is valid")
            form.save()
            return redirect('base')
        else :
            print("form is not valid")
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile/profile.html', {'form': form})

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm

@login_required
def profile_details(request):
    profile = get_object_or_404(Profile, user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('base')
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'profile/profile_details.html', {'form': form, 'profile': profile})

@login_required
def payment_details(request):
    return render(request, 'payment_details.html')

def register_trade(request):
    if request.method == 'POST':
        form = TradeForm(request.POST)
        if form.is_valid():
            trade = form.save(commit=False)
            trade.user = request.user
            trade.save()
            # Update performance metrics here
            update_performance_metrics(request.user)
            return redirect('base')
    else:
        form = TradeForm()
    return render(request, 'core/register_trade.html', {'form': form})
from django.http import JsonResponse
import requests
from datetime import datetime

import requests
from django.http import JsonResponse
import datetime

def get_prices(request):
    try:
        # CoinGecko (BTC, ETH)
        crypto_res = requests.get(
            "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
        ).json()

        # Exchangerate.host (Forex + Gold)
        forex_res = requests.get(
            "https://api.exchangerate.host/latest?base=USD&symbols=UZS,JPY,EUR,XAU"
        ).json()

        prices = {
            "BTC/USD": crypto_res["bitcoin"]["usd"],
            "ETH/USD": crypto_res["ethereum"]["usd"],
            "USD/UZS": round(forex_res["rates"]["UZS"], 2),
            "USD/JPY": round(forex_res["rates"]["JPY"], 2),
            "EUR/USD": round(1 / forex_res["rates"]["EUR"], 4),
            "XAU/USD": round(1 / forex_res["rates"]["XAU"], 2),  # Oltin narxi
        }

    except Exception as e:
        prices = {"error": str(e)}

    return JsonResponse({
        "prices": prices,
        "updated": datetime.datetime.now().strftime("%H:%M:%S")
    })
import requests
from django.shortcuts import render

def economic_calendar(request):
    api_key = "8YWGDSEMSE2MWQAJ"
    url = f"https://www.alphavantage.co/query?function=ECONOMIC_CALENDAR&apikey={api_key}"

    response = requests.get(url)
    data = response.json()

    events = data.get("economicCalendar", [])

    return render(request, "calendar.html", {"events": events})
# views.py
import requests
from django.shortcuts import render

FRED_API_KEY = "ffd6b8148d9935750f35bf5e3a201164"

# FRED indikatorlarini sozlash
FRED_SERIES = {
    "NFP (Nonfarm Payrolls)": "PAYEMS",
    "CPI (Inflation)": "CPIAUCSL",
    "GDP": "GDP",
    "Federal Funds Rate": "FEDFUNDS",
    "Unemployment Rate": "UNRATE"
}

def economic_calendar(request):
    events = []

    for name, series_id in FRED_SERIES.items():
        url = "https://api.stlouisfed.org/fred/series/observations"
        params = {
            "series_id": series_id,
            "api_key": FRED_API_KEY,
            "file_type": "json",
            "sort_order": "desc",
            "limit": 2  # oxirgi 2 ta qiymat (oldingi + yangi)
        }
        try:
            res = requests.get(url, params=params)
            data = res.json().get("observations", [])

            if len(data) >= 2:
                latest = data[-1]   # oxirgi
                previous = data[-2] # oldingi

                events.append({
                    "date": latest.get("date"),
                    "country": "🇺🇸 AQSH",
                    "event": name,
                    "forecast": "-",  # FRED forecast bermaydi
                    "previous": previous.get("value"),
                    "actual": latest.get("value"),
                })
        except Exception as e:
            print(f"Xato: {e}")

    return render(request, "economic_calendar.html", {"events": events})



@login_required
def calendar__(request):
    return render(request, 'calendar.html')