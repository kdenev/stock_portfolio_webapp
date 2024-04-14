from yahooquery import Ticker, search
from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Declare constants
ETF_COMPONETS_URL = os.environ['ETF_COMPONETS_URL']
SELECT_COLUMNS = ['Id', 'Name', 'Ticker', 'Identifier']

# Create a class to fetch the symbol data and create sql db
class StockBase():
    def __init__(self):
        self.read_data()
        self.search_df = pd.DataFrame()
        self.engine = create_engine('sqlite:///instance/ticker_info.db')
        
    def read_data(self):
        self.data = pd.read_excel(ETF_COMPONETS_URL, skiprows=4, skipfooter=61)
        self.data = self.data.loc[self.data['Ticker'] != '-']
        self.data['Ticker'] = self.data['Ticker'].apply(lambda x: x.replace('.', '-'))
        self.data['Id'] = list(range(1,len(self.data)+1))
        self.etf_components = self.data[SELECT_COLUMNS].rename({'Identifier':'ISIN'})

    def write_to_db(self):
        self.etf_components.to_sql('ticker_info', self.engine, if_exists='replace', index=False)

    def fetch_details(self):
        pass

# Fetch the data
stock_info = StockBase()
stock_info.write_to_db()