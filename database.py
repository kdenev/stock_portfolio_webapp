from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text

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