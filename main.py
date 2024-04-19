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
    query = sa.select(Ratios)
    data = db.paginate(query, page=page, per_page=40, error_out=False)
    next_url = None
    prev_url = None
    if data.has_next:
        next_url = url_for('home', page=data.next_num)
    if data.has_prev:
        prev_url = url_for('home', page=data.prev_num)
    return render_template('home.html'
                           , data=data.items
                           , column_names = query.subquery().columns.keys()
                           , page=page
                           , next_url=next_url
                           , prev_url=prev_url
                        )

@app.route('/process_selection', methods=['POST'])
def process_selection():
    selected_rows = request.form.getlist('selected_rows')  # Retrieves all selected row identifiers
    # Process the selected rows as needed
    print(selected_rows)  # For demonstration, just print the selected rows
    
    return redirect(url_for('home'))  # Redirect back to the table view or to another page

@app.route('/sort_table', methods=['POST', 'GET'])
def sort_table():
    print("Table sorting processe!")
    if request.method == 'POST':
        print('In post!')
        print(request.form['form1'])
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True, port=5033)