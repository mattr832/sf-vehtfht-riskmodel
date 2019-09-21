#importing libraries
import os
import json
import flask
from flask import Flask, render_template, request, jsonify
from sf_vehthft_utils import *

#creating instance of the class
app=flask.Flask(__name__)

def run_constraints(jsondata):
    if check_lat(jsondata['Latitude']) == 0:
        return {'Latitude Error': '''Bro, you're not parked in San Fran'''}
    elif check_long(jsondata['Longitude']) == 0:
        return {'Longitude Error': '''Bro, you're not parked in San Fran'''}
    else: 
        return get_risk(jsondata)
    
@app.route('/',methods = ['POST'])
def result():
    if request.method == 'POST':
        to_predict_list = request.get_json()
        #run lat long checks, return message if they fail, else get pred
        response = run_constraints(to_predict_list)
        #return the result
        return jsonify(response)
    
# Start the server, continuously listen to requests.
if __name__=="__main__":
    # For local development, set to True:
    # app.run(debug=True)
    # For public web serving:
    app.run(host='97.113.5.182')
    app.run()
