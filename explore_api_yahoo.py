from yahooquery import Ticker
import pandas as pd

t_object = Ticker(['AAPL'])


# Summary data
ratios = ['previousClose', 'payoutRatio', 'beta', 'trailingPE', 'forwardPE', 'dividendYield']
summary_data = pd.DataFrame(t_object.summary_detail).transpose()[ratios].reset_index().rename(columns={'index':'symbol'})

# Financial data time series
financial_items = ['symbol', 'year', 'TotalDebt', 'CashAndCashEquivalents', 'NormalizedEBITDA', 'NormalizedIncome']
fin_data = pd.DataFrame(t_object.all_financial_data())
fin_data['year'] = fin_data.asOfDate.dt.strftime('%Y')
fin_data_processed = fin_data.reset_index()[financial_items]
# Financial data ratios
t_object.financial_data


# Key Ratios
key_ratios = ['trailingEps', 'pegRatio', 'enterpriseToEbitda', 'priceToBook']
key_data = pd.DataFrame(t_object.key_stats).transpose()[key_ratios].reset_index().rename(columns={'index':'symbol'})
# News
# Decent for some companies, old data for others
# No link to the full article though
# Latest news for Apple 2023-08-14
t_object.corporate_events.reset_index()
t_object.news(5)
