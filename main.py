from flask import Flask, abort, render_template, redirect, url_for, flash, request, jsonify
from flask_bootstrap import Bootstrap5
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
import sqlalchemy as sa
from database import db, TickerInfo, Ratios
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
    page = request.args.get('page', 1, type=int)
    sort_var = request.args.get('sort_var', None, type=str)
    query = sa.select(Ratios).order_by(sort_var)
    data = db.session.execute(query).scalars()
    # next_url = None
    # prev_url = None
    # if data.has_next:
    #     next_url = url_for('home', page=data.next_num)
    # if data.has_prev:
    #     prev_url = url_for('home', page=data.prev_num)
    return render_template('home.html'
                           , data=data
                           , column_names = query.subquery().columns.keys()
                           , page=page
                        #    , next_url=next_url
                        #    , prev_url=prev_url
                        )

@app.route('/sort_page', methods=['POST', 'GET'])
def sort_page():
    sort_var = request.args.get('sort_var', None, type=str)
    data = request.args.get('data', None, type=str)
    print(data[4])
    return redirect(url_for('home', data=data))


if __name__ == "__main__":
    app.run(debug=True, port=5033)