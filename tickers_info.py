from yahooquery import Ticker, search
from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

#TODO
# Download world index components from this link
# https://www.ssga.com/se/en_gb/institutional/etfs/library-content/products/fund-data/etfs/emea/holdings-daily-emea-en-sppw-gy.xlsx
#TODO
# Use the search function to get the basic information for each stock
#TODO
# Create relational database with the available information

ETF_COMPONETS_URL = os.environ['ETF_COMPONETS_URL']
SEARCH_COLUMNS = ['exchange', 'shortname', 'symbol', 'longname']

# response = search('US0378331005')
# response['quotes']

class StockBase():
    def __init__(self):
        self.read_data()
        self.search_df = pd.DataFrame()
        self.engine = create_engine('sqlite:///instance/ticker_info.db')
        
    def read_data(self):
        self.data = pd.read_excel(ETF_COMPONETS_URL, skiprows=5, skipfooter=1)
        self.etf_components = self.data[self.data['ISIN'] != 'Unassigned'].dropna()

    def search_info(self, isin):
        return pd.DataFrame(search(isin)['quotes'])[SEARCH_COLUMNS]
    
    def compile_search_results(self):
        for isin in self.etf_components['ISIN'][:5]:
            row = self.search_info(isin)
            row['isin'] = isin
            self.search_df = pd.concat([self.search_df, row])
        return self.search_df
    
    def write_to_db(self):
        self.search_df.to_sql('ticker_info', self.engine, if_exists='replace', index=False)

stock_info = StockBase()
stock_info.compile_search_results()
stock_info.write_to_db()