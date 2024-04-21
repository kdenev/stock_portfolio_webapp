from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, Float

# CREATE DATABASE
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# CONFIGURE TABLES
class TickerInfo(db.Model):
    __tablename__ = "ticker_info"
    symbol: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    isin: Mapped[str] = mapped_column(String, nullable=False)

class Ratios(db.Model):
    __tablename__ = "ratios"
    symbol: Mapped[str] = mapped_column(String, primary_key=True)
    sector: Mapped[str] = mapped_column(String, nullable=True)
    industry: Mapped[str] = mapped_column(String, nullable=True)
    fulltimeemployees: Mapped[str] = mapped_column(String, nullable=True)
    targetmeanprice: Mapped[float] = mapped_column(Float, nullable=True)
    numberofanalystopinions: Mapped[int] = mapped_column(Integer, nullable=True)
    recommendationkey: Mapped[str] = mapped_column(String, nullable=True)
    trailingeps: Mapped[float] = mapped_column(Float, nullable=True)
    pegratio: Mapped[float] = mapped_column(Float, nullable=True)
    enterprisetoebitda: Mapped[float] = mapped_column(Float, nullable=True)
    enterprisetorevenue: Mapped[float] = mapped_column(Float, nullable=True)
    pricetobook: Mapped[float] = mapped_column(Float, nullable=True)
    payoutratio: Mapped[float] = mapped_column(Float, nullable=True)
    beta: Mapped[float] = mapped_column(Float, nullable=True)
    trailingpe: Mapped[float] = mapped_column(Float, nullable=True)
    dividendyield: Mapped[float] = mapped_column(Float, nullable=True)