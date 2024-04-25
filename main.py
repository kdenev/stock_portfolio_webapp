from flask import Flask, abort, render_template, redirect, url_for, flash, request, jsonify
from flask_bootstrap import Bootstrap5
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
import sqlalchemy as sa
from database import db, TickerInfo, Ratios
from forms import FilterTable
import os
import numpy as np
import pandas as pd
# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
# app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'darkly'
Bootstrap5(app)

# DATA
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    form = FilterTable()
    if form.validate_on_submit():
        print('Form submitted')
    page = request.args.get('page', 1, type=int)
    sort_var = request.args.get('sort_var', None, type=str)
    sector = request.args.get('sector', None, type=str)
    query = sa.select(Ratios).order_by(sort_var)
    column_names = query.subquery().columns.keys()
    if sector:
        query = sa.select(Ratios).where(Ratios.sector == sector)
        data = db.session.execute(query).scalars()
    data = db.session.execute(query).scalars()
    sector_query = sa.select(sa.distinct(Ratios.sector))
    sectors = db.session.execute(sector_query).scalars()
    return render_template('home.html'
                           , data=data
                           , column_names = column_names
                           , page=page
                           , sectors = sectors
                           , form=form
                        )

@app.route('/sector_filter', methods=['POST', 'GET'])
def sector_filter():
    sector = request.args.get('sector', None, type=str)
    query = sa.select(Ratios).where(Ratios.sector == sector)
    data = db.session.execute(query).__dict__
    print(data)
    return data

if __name__ == "__main__":
    app.run(debug=True, port=5033)