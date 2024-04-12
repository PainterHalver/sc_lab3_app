#!/usr/bin/env python3

from flask import Flask, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os
from flask_cors import CORS
import boto3

from config import DATABASE_URI

app = Flask(__name__, static_folder='client/build')
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
db = SQLAlchemy(app)
app.app_context().push()
client = boto3.client('s3')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')
    
@app.route('/api/check_sg')
def boto():
  buckets = client.list_buckets()
  return jsonify(buckets)

@app.route('/api/csv')
def quotes():
  from models import Quote
  quotes = Quote.query.all()
  return jsonify([quote.to_dict() for quote in quotes])
