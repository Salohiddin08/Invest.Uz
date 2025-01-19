import requests

# Get live cryptocurrency prices
def get_crypto_prices():
    url = "https://api.coingecko.com/api/v3/simple/price"#- this API for the crytpo news 
    params = {"ids": "bitcoin,ethereum,cardano", "vs_currencies": "usd"}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {}
    
# Get news for a specific cryptocurrency
def get_crypto_news(coin_name):
    url = f"https://newsapi.org/v2/everything"
    params = {
        "q": coin_name,
        "apiKey": "--------------------------", #- go to to the wibsite (newsapi.org) signup and get the API key
        "language": "en",
        "pageSize": 5
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("articles", [])
    else:
        return []
    