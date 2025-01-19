"""
URL configuration for backtesting project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
# from views import base, aboutus, settings, index, contact

urlpatterns = [
    path('tradeslog/',views.tradeslog, name="tradeslog"),
    path('', views.base, name="base"),
    path('payment_details/', views.payment_details, name='payment_details'),
    path('performance_chart/', views.performance_chart, name='performance_chart'),
    path('strategyoverview/', views.strategyoverview, name="strategyoverview"),
    path("performanceanalytics/", views.performanceanalytics, name="performanceanalytics"),
    path('start_streamlit/', views.start_streamlit, name='start_streamlit'),  # Add this line
    path('news/bitcoin/', views.news_bitcoin, name='news_bitcoin'),
    path('news/ethereum/', views.news_ethereum, name='news_ethereum'),
    path('news/ripple/', views.news_ripple, name='news_ripple'),
    path('news/litecoin/', views.news_litecoin, name='news_litecoin'),
    path('news/cardano/', views.news_cardano, name='news_cardano'),
    #- for the signup and login
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view, name='profile'),  # Assuming you have a profile view 
    path('logout/', views.logout_view, name='logout'),
    #- adding the termsn and conditions
    # path('termsandconditions/', views.termsandconditions, name='termsandconditions'),
    path('backtesting/', views.landingpage, name='landingpage'),
    path('profile_details/', views.profile_details, name='profile_details'),
    path("crypto/prices/", views.crypto_prices_view, name="crypto-prices"),
    path("crypto/news/<str:coin_name>/", views.crypto_news_view, name="crypto-news"),
    path("metrics/calculate/", views.calculate_metrics_view, name="calculate-metrics"),
]
