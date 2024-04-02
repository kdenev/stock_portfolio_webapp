from dotenv import load_dotenv
import requests
import os

# Load env variables
load_dotenv()
print(os.environ['ALPHA_KEY'])
# Check if can get information in batches
url = 'https://www.alphavantage.co/query'
params = {
    "function": "INCOME_STATEMENT"
    , "symbol": ["IBM", "MSFT"]
    , "apikey": os.environ['ALPHA_KEY'] 
}

r = requests.get(url, params=params)
data = r.json()

print(data)

# Needed columns

# OVERVIEW
# Symbol, Name, Sector, Industry, Country, EPS, Exchange
# , Currency, EPS, EBITDA, PERatio(TrailingPE, ForwardPE)
# , DividendYield, AnalystTargetPrice, EVToEBITDA, PriceToBookRatio
# , Beta, PEGRatio

# BALANCE_SHEET
# "quarterlyReports"[0]
# fiscalDateEnding, shortLongTermDebtTotal, cashAndCashEquivalentsAtCarryingValue

# INCOME_STATEMENT
# "annualReports"[:5]
# fiscalDateEnding, ebit, ebitda, netIncome

# EARNINGS
# quarterlyEarnings[:4]
# reportedEPS, surprisePercentage