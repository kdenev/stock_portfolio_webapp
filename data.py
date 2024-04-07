from yahooquery import Ticker, search
import pandas as pd

#TODO
# Download world index components from this link
# https://www.ssga.com/se/en_gb/institutional/etfs/funds/spdr-msci-world-ucits-etf-sppw-gy
#TODO
# Use the search function to get the basic information for each stock
#TODO
# Create relational database with the available information



class DataQery(Ticker):
    def __init__(self, symbols, **kwargs):
        super().__init__(symbols, **kwargs)
        