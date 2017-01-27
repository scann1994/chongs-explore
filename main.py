# Imports
import os
import jinja2
import webapp2
import logging
import json
import urllib

# this is used for constructing URLs to google's APIS
from googleapiclient.discovery import build

# This uses discovery to create an object that can talk to the 
# fusion tables API using the developer key
#service = build('fusiontables', 'v1', developerKey=API_KEY)

from flask import Flask
app = Flask(__name__)
app.config['DEBUG'] = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
