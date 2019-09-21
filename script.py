#importing libraries
import os
import json
import flask
from flask import Flask, render_template, request, jsonify
from sf_vehthft_utils import *

#creating instance of the class
app=flask.Flask(__name__)

    
@app.route('/',methods = ['POST'])
def result():
    if request.method == 'POST':
        to_predict_list = request.get_json()
        #run the get_risk function from the utils module
        response = get_risk(to_predict_list)
        #return the result
        return jsonify(response)
    
# Start the server, continuously listen to requests.
if __name__=="__main__":
    # For local development, set to True:
    # app.run(debug=False)
    # For public web serving:
    app.run(host='97.113.5.182')
    app.run()
