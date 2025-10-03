from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # 🔹 Narxlar uchun endpoint
    path("get-prices/", views.get_prices, name="get_prices"),

    # 🔹 Asosiy sahifalar
    path('tradeslog/', views.tradeslog, name="tradeslog"),
    path('', views.base, name="base"),
    path('payment_details/', views.payment_details, name='payment_details'),
    path('performance_chart/', views.performance_chart, name='performance_chart'),
    path('strategyoverview/', views.strategyoverview, name="strategyoverview"),
    path("performanceanalytics/", views.performanceanalytics, name="performanceanalytics"),
    path('start_streamlit/', views.start_streamlit, name='start_streamlit'),

    # 🔹 Kripto yangiliklar
    path('news/bitcoin/', views.news_bitcoin, name='news_bitcoin'),
    path('news/ethereum/', views.news_ethereum, name='news_ethereum'),
    path('news/ripple/', views.news_ripple, name='news_ripple'),
    path('news/litecoin/', views.news_litecoin, name='news_litecoin'),
    path('news/cardano/', views.news_cardano, name='news_cardano'),

    # 🔹 Auth (signup / login / profile / logout)
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),

    # 🔹 Boshqa sahifalar
    path('backtesting/', views.landingpage, name='landingpage'),
    path('profile_details/', views.profile_details, name='profile_details'),

    # 🔹 API endpointlare
    path("crypto/prices/", views.crypto_prices_view, name="crypto-prices"),
    path("crypto/news/<str:coin_name>/", views.crypto_news_view, name="crypto-news"),
    path("metrics/calculate/", views.calculate_metrics_view, name="calculate-metrics"),
    path("calendar/", views.calendar__, name="calendar___"),
    path("chart/", views.chart, name="chart")
    ]
