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
class StockBase(Ticker):
    def __init__(self, symbols = None, **kwargs):
        super().__init__(symbols, **kwargs)
        self.read_data()
        self.search_df = pd.DataFrame()
        self.symbols = self.etf_components['Ticker'][:10]
        self.summary_data_columns = ['previousClose', 'payoutRatio', 'beta', 'trailingPE', 'dividendYield']
        self.sumamry_profile_columns = ['industry', 'sector', 'fullTimeEmployees']
        self.financial_data_columns = ['symbol', 'year', 'TotalDebt', 'CashAndCashEquivalents', 'NetDebt', 'NormalizedEBITDA', 'NormalizedIncome']
        self.financial_ratios_columns = ['targetMeanPrice', 'numberOfAnalystOpinions', 'recommendationKey']
        self.key_ratios_columns = ['trailingEps', 'pegRatio', 'enterpriseToEbitda', 'enterpriseToRevenue', 'priceToBook']
        
    def read_data(self):
        self.data = pd.read_excel(ETF_COMPONETS_URL, skiprows=4, skipfooter=61)
        self.data = self.data.loc[self.data['Ticker'] != '-']
        self.data['Ticker'] = self.data['Ticker'].apply(lambda x: x.replace('.', '-'))
        self.data['Id'] = list(range(1,len(self.data)+1))
        self.etf_components = self.data[SELECT_COLUMNS].rename({'Identifier':'ISIN'})

    def write_to_db(self, data, name):
        self.engine = create_engine(f'sqlite:///instance/{name}.db')
        data.to_sql(name, self.engine, if_exists='replace', index=False)

    def fetch_summary_details(self):
        summary_details = (
                            pd.DataFrame(self.summary_detail)
                            .transpose()[self.summary_data_columns]
                            .reset_index()
                            .rename(columns={'index':'symbol'})
                        )
        summary_profile = (
                            pd.DataFrame(self.summary_profile)
                            .transpose()[self.sumamry_profile_columns]
                            .reset_index()
                            .rename(columns={'index':'symbol'})
                        )
        self.summary_data = summary_details.merge(summary_profile, on='symbol', how='inner')
        return self.summary_data
    
    def fetch_ratio_data(self):
        financial_ratios = (
                            pd.DataFrame(self.financial_data)
                            .transpose()[self.financial_ratios_columns]
                            .reset_index()
                            .rename(columns={'index':'symbol'})
                        )
        key_ratios = (
                      pd.DataFrame(self.key_stats)
                      .transpose()[self.key_ratios_columns]
                      .reset_index()
                      .rename(columns={'index':'symbol'})
                    )
        self.ratios_data = financial_ratios.merge(key_ratios, on='symbol', how='inner')
        return self.ratios_data
        #TODO create time 2 new ralational databases. 
        # 1 for the discrete values
        # 2 for the continuos values(balance sheet information)

# Fetch the data
stock_info = StockBase()
stock_info.fetch_summary_details()
stock_info.fetch_ratio_data()
stock_info.summary_detail
a = stock_info.fetch_details()
summary_data = a.summary_detail
summary_data_columns = ['previousClose', 'payoutRatio', 'beta', 'trailingPE', 'dividendYield']
sumamry_profile_columns = ['industry', 'sector', 'fullTimeEmployees']
# , 'forwardPE'
pd.DataFrame(summary_data).transpose()[summary_data_columns].reset_index().rename(columns={'index':'symbol'})

a = Ticker('AAPL')
pd.DataFrame(a.summary_profile).T[['industry', 'sector', 'fullTimeEmployees']]
financial_data_columns = ['symbol', 'year', 'TotalDebt', 'CashAndCashEquivalents', 'NetDebt', 'NormalizedEBITDA', 'NormalizedIncome']
fin_data = pd.DataFrame(a.all_financial_data())
fin_data['year'] = fin_data.asOfDate.dt.strftime('%Y')
fin_data['NetDebt'] = fin_data['TotalDebt'] - fin_data['CashAndCashEquivalents']
fin_data_processed = fin_data.reset_index()[financial_data_columns]
fin_data_processed

fin_items_extra = ['targetMeanPrice', 'numberOfAnalystOpinions', 'recommendationKey']
fin_data_extra = pd.DataFrame(a.financial_data).transpose()[fin_items_extra].reset_index().rename(columns={'index':'symbol'})

# Key Ratios
key_ratios = ['trailingEps', 'pegRatio', 'enterpriseToEbitda', 'priceToBook']
key_data = pd.DataFrame(a.key_stats).transpose()[key_ratios].reset_index().rename(columns={'index':'symbol'})