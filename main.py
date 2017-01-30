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
    
API_KEY = AIzaSyAuLSYsTH7R8qWEYmVu0F5EjC_6WmCPV_0
TABLE_ID = '1JobEuJSRuLuxxXgMXrVOdgPA7K9FMJVdOYZ3SgQ'

# This uses discovery to create an object that can talk to the 
# fusion tables API using the developer key
service = build('fusiontables', 'v1', developerKey=API_KEY)



# Import the Flask Framework
from flask import Flask
app = Flask(__name__)
app.config['DEBUG'] = True

def get_all_data(query):
	#request = service.table().get(tableId=TABLE_ID) 
	response = service.query().sql(sql=query).execute()
	return response

# Default columns for the query
query_cols = []
query_animals = ['China']

# make a query given a set of columns to retrieve
def make_query(cols, countries, limit):
	string_cols = ""
	if cols == []:
		cols = ['*']
	for col in cols:
		string_cols = string_cols + ", " + col
	string_cols = string_cols[2:len(string_cols)] #why start with second?
	
	string_countries = ""
	for country in countries:
		string_countries = string_countries + country
	string_countries = string_countries[2:len(string_countries)]
	
	query = "SELECT" + string_cols + " FROM " + TABLE_ID + " WHERE Country = '" + string_countries + "'"
	query = query + " LIMIT " + str(limit)
	
	logging.info(query)
	return query


@app.route('/')
def get_all_data(self):
    query = "SELECT * FROM " + TABLE_ID + " WHERE  Country = 'China' LIMIT 2"
    response = service.query().sql(sql=query).execute()
    logging.info(response['columns'])
    logging.info(response['rows'])
        
    return response


#@app.route('/')
#def index():
#    template = JINJA_ENVIRONMENT.get_template('templates/index.html')
#    request = service.column().list(tableId = TABLE_ID)
#    allheaders = get_all_data(make_query([], query_countries, 1))
#    logging.info('allheaders') #what is logging.info?
#    return template.render(allheaders = allheaders['columns'])


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
