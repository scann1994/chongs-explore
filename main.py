# Imports
import os
import jinja2
import webapp2
import logging
import json
import urllib

# this is used for constructing URLs to google's APIS
from googleapiclient.discovery import build

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

# This API key is provided by google as described in the tutorial
API_KEY = 'AIzaSyB_-NGJMfYUSzHy0JTsnK_CSkkqdvwerDU'


# This uses discovery to create an object that can talk to the 
# fusion tables API using the developer key
service = build('fusiontables', 'v1', developerKey=API_KEY)

# This is the table id for the fusion table
TABLE_ID = '1BOY_Wi7d89TcGVEv2r7GdgaA7oCqS7NuxdSDyZ9e'

# This is the default columns for the query
query_cols = []
query_countries = ['China']

# Import the Flask Framework
from flask import Flask, request
app = Flask(__name__)

def get_all_data(query):
    response = service.query().sql(sql=query).execute()
    return response

# make a query given a set of columns to retrieve
def make_query(cols, countries, limit):
    string_cols = ""
    if cols == []:
        cols = ['*']
    for col in cols:
        string_cols = string_cols + ", " + col
    string_cols = string_cols[2:len(string_cols)]

    string_countries = ""
    for country in countries:
        string_countries = string_countries + ", " + country
    string_countries = string_countries[2:len(string_countries)]
    
    query = "SELECT " + string_cols + " FROM " + TABLE_ID + " WHERE Country = '" + string_countries + "'"

    query = query + " LIMIT " + str(limit)

    logging.info(query)
    # query = "SELECT * FROM " + TABLE_ID + " WHERE  Country = 'China' LIMIT 2"

    return query
    
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

@app.route('/')
def index():
    template = JINJA_ENVIRONMENT.get_template('templates/index.html')
    logging.info(':(')
    request = service.column().list(tableId=TABLE_ID)
    allheaders = get_all_data(make_query([], query_countries, 1))
    logging.info('allheaders')
    return template.render(allheaders=allheaders['columns'] )

@app.route('/_update_table', methods=['POST']) 
def update_table():
    logging.info(request.get_json())
    cols = request.json['cols']
    logging.info(cols)
    result = get_all_data(make_query(cols, query_countries, 100))
    logging.info(result)
    return json.dumps({'content' : result['rows'], 'headers' : result['columns']})

@app.route('/about')
def about():
    template = JINJA_ENVIRONMENT.get_template('templates/about.html')
    return template.render()

@app.route('/quality')
def quality():
    template = JINJA_ENVIRONMENT.get_template('templates/quality.html')
    return template.render()

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404

@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
