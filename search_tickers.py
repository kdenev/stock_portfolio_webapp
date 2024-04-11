from yahooquery import Ticker, search
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text

#TODO
# Download world index components from this link
# https://www.ssga.com/se/en_gb/institutional/etfs/library-content/products/fund-data/etfs/emea/holdings-daily-emea-en-sppw-gy.xlsx
#TODO
# Use the search function to get the basic information for each stock
#TODO
# Create relational database with the available information

ETF_COMPONETS_URL = "https://www.ssga.com/se/en_gb/institutional/etfs/library-content/products/fund-data/etfs/emea/holdings-daily-emea-en-sppw-gy.xlsx"
SEARCH_COLUMNS = ['exchange', 'shortname', 'symbol', 'longname', 'sector', 'industry']

# response = search('US0378331005')
# response['quotes']

class StockBase():
    def __init__(self):
        self.read_data()
        
    def read_data(self):
        self.data = pd.read_excel(ETF_COMPONETS_URL, skiprows=5, skipfooter=1)
        self.etf_components = self.data[self.data['ISIN'] != 'Unassigned'].dropna()

    def search_info(self, isin):
        return pd.DataFrame(search(isin)['quotes'])[SEARCH_COLUMNS][:10]
    
    def compile_search_results(self):
        self.search_df = pd.DataFrame()
        for isin in self.etf_components['ISIN']:
            row = self.search_info(isin)
            row['isin'] = isin
            self.search_df = pd.concat[self.search_df, row]
        return self.search_df


# CREATE DATABASE
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# CONFIGURE TABLES
class CompanyInfo(db.Model):
    __tablename__ = "comp_info"
    # 'id', 'exchange', 'shortname', 'symbol', 'longname', 'sector', 'industry'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    isin: Mapped[str] = mapped_column(String, nullable=False)
    symbol: Mapped[str] = mapped_column(String, nullable=False)
    exchange: Mapped[str] = mapped_column(String, nullable=False)
    shortname: Mapped[str] = mapped_column(String, nullable=False)
    longname: Mapped[str] = mapped_column(String, nullable=False)
    sector: Mapped[str] = mapped_column(String, nullable=False)
    industry: Mapped[str] = mapped_column(String, nullable=False)