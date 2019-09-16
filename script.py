#importing libraries
import os
import flask
from flask import Flask, render_template, request
from sf_vehthft_utils import *
from sf_vehthft_getmap import *

#creating instance of the class
app=flask.Flask(__name__)

#to tell flask what url should trigger the function index()
@app.route('/')
@app.route('/index')
def index():
    return flask.render_template('index.html')
    
@app.route('/result',methods = ['POST'])
def result():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        #run the get_risk function from the utils module
        response = get_risk(to_predict_list)
        #get map with marker html and save into the templates folder
        get_map(response)
        #return the result
        return render_template("result.html", response=response)
    
# Start the server, continuously listen to requests.
if __name__=="__main__":
    # For local development, set to True:
    app.run(debug=True)
    # For public web serving:
    #app.run(host='0.0.0.0')
    app.run()
