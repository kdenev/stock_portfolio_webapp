from dotenv import load_dotenv
import requests
import os

# Load env variables
load_dotenv()
print(os.environ['TIINGO_KEY'])
# Only dow 30 tickers even for paid users
# all tickers at extra charge
url = 'https://api.tiingo.com/tiingo/fundamentals/definitions'

headers = {
    'Content-Type': 'application/json'
}

params = {
    "token": os.environ['TIINGO_KEY'] 
}

r = requests.get(url, params=params, headers=headers)
data = r.json()

print(data)

