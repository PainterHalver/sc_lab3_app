#!/usr/bin/env python3

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import boto3

from config import DATABASE_URI

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
db = SQLAlchemy(app)
app.app_context().push()
client = boto3.client('s3')

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/boto')
def boto():
  buckets = client.list_buckets()
  return jsonify(buckets)

@app.route('/quotes')
def quotes():
  from models import Quote
  quotes = Quote.query.all()
  return jsonify([quote.to_dict() for quote in quotes])