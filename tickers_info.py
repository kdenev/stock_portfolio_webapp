from yahooquery import Ticker, search
from sqlalchemy import create_engine, text
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Declare constants
ETF_COMPONETS_URL = os.environ['ETF_COMPONETS_URL']
SELECT_COLUMNS = ['Name', 'Ticker', 'Identifier']
DB_RATIOS = "ratios"
DB_FUNDAMENTALS = "fundamentals"
DB_TICKER = "ticker_info"

# Create a class to fetch the symbol data and create sql db
class StockBase(Ticker):
    def __init__(self, symbols = None, **kwargs):
        super().__init__(symbols, **kwargs)
        self.read_data()
        self.search_df = pd.DataFrame()
        self.symbols = self.etf_components['symbol']
        self.summary_data_columns = ['previousClose', 'payoutRatio', 'beta', 'trailingPE', 'dividendYield']
        self.sumamry_profile_columns = ['industry', 'sector', 'fullTimeEmployees']
        self.financial_data_columns = ['symbol', 'year', 'TotalDebt', 'CashAndCashEquivalents', 'NetDebt', 'NormalizedEBITDA', 'NormalizedIncome']
        self.financial_ratios_columns = ['targetMeanPrice', 'numberOfAnalystOpinions', 'recommendationKey']
        self.key_ratios_columns = ['trailingEps', 'pegRatio', 'enterpriseToEbitda', 'enterpriseToRevenue', 'priceToBook']
        
    def read_data(self):
        self.data = pd.read_excel(ETF_COMPONETS_URL, skiprows=4, skipfooter=61)
        self.data = self.data.loc[self.data['Ticker'] != '-']
        self.data['Ticker'] = self.data['Ticker'].apply(lambda x: x.replace('.', '-'))
        # self.data['Id'] = list(range(1,len(self.data)+1))
        self.etf_components = self.data[SELECT_COLUMNS]
        self.etf_components = self.etf_components.rename(columns={'Ticker': 'symbol'
                                                        , 'Name':'name'
                                                        , 'Identifier':'isin'
                                                    })
        
    def write_to_db(self, data, name):
        self.engine = create_engine(f'sqlite:///instance/comp_info.db')
        data.to_sql(name, self.engine, if_exists='replace', index=False)

    def fetch_summary_details(self):
        summary_details = (
                            pd.DataFrame(self.summary_detail)
                            .transpose()[self.summary_data_columns]
                            .reset_index()
                            .rename(columns={'index':'symbol'})
                            .rename(columns={col:col.lower() for col in self.summary_data_columns})
                        )
        summary_profile = (
                            pd.DataFrame(self.summary_profile)
                            .transpose()[self.sumamry_profile_columns]
                            .reset_index()
                            .rename(columns={'index':'symbol'})
                            .rename(columns={col:col.lower() for col in self.sumamry_profile_columns})
                        )
        self.summary_data = summary_details.merge(summary_profile, on='symbol', how='inner')
        return self.summary_data
    
    def fetch_ratio_data(self):
        financial_ratios = (
                            pd.DataFrame(self.financial_data)
                            .transpose()[self.financial_ratios_columns]
                            .reset_index()
                            .rename(columns={'index':'symbol'})
                            .rename(columns={col:col.lower() for col in self.financial_ratios_columns})
                        )
        key_ratios = (
                      pd.DataFrame(self.key_stats)
                      .transpose()[self.key_ratios_columns]
                      .reset_index()
                      .rename(columns={'index':'symbol'})
                      .rename(columns={col:col.lower() for col in self.key_ratios_columns})
                    )
        self.ratios_data = financial_ratios.merge(key_ratios, on='symbol', how='inner')
        return self.ratios_data
    
    def fetch_fundamentals_data(self):
        fundamentals_data = pd.DataFrame(self.all_financial_data())
        fundamentals_data['year'] = fundamentals_data.asOfDate.dt.strftime('%Y')
        fundamentals_data['NetDebt'] = fundamentals_data['TotalDebt'] - fundamentals_data['CashAndCashEquivalents']
        self.fundamentals_data_processed = fundamentals_data.reset_index()[self.financial_data_columns]
        self.fundamentals_data_processed = self.fundamentals_data_processed.rename(columns={col:col.lower() for col in self.financial_data_columns})
        return self.fundamentals_data_processed

    def write_db_ratios(self):
        self.fetch_ratio_data()
        self.fetch_summary_details()
        self.ratios_data = self.ratios_data.merge(self.summary_data, on='symbol', how='inner')
        self.write_to_db(self.ratios_data, DB_RATIOS)

    def write_db_fundamentals(self):
        self.fetch_fundamentals_data()
        self.write_to_db(self.fundamentals_data_processed, DB_FUNDAMENTALS)

    def write_db_ticker_info(self):
        self.write_to_db(self.etf_components, DB_TICKER)

# Fetch the data
stock_info = StockBase()
stock_info.write_db_ticker_info()
stock_info.write_db_fundamentals()
stock_info.write_db_ratios()