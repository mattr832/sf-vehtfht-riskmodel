#importing libraries
import os
import json
import pickle
import datetime
from pytz import timezone
import pytz
import flask
from flask import Flask, render_template, request, jsonify
from sf_vehthft_utils import *

#creating instance of the class
app=flask.Flask(__name__)


# load the label encoders from disk
pdistrict_labenc = pickle.load(open('pdistrict_labenc.pkl', 'rb'))
sdistrict_labenc = pickle.load(open('sdistrict_labenc.pkl', 'rb'))
hood_labenc = pickle.load(open('hood_labenc.pkl', 'rb'))
inter_labenc = pickle.load(open('inter_labenc.pkl', 'rb'))

# load the preprocessing models from disk
pdistrict_knn = pickle.load(open('pdistrict_knn.pkl', 'rb'))
sdistrict_lgbm = pickle.load(open('sdistrict_lgbm.pkl', 'rb'))
hood_knn = pickle.load(open('hood_knn.pkl', 'rb'))
inter_knn = pickle.load(open('inter_knn.pkl', 'rb'))
    
@app.route('/',methods = ['POST'])
def result():
    if request.method == 'POST':
        #get current datetime from POST request
        currentDT = datetime.now(tz=pytz.utc).replace(microsecond=0)
        currentDT = currentDT.astimezone(timezone('US/Pacific'))
        cdt = str(currentDT)
        cdt = cdt[:19]
        #get paramters from URL request
        lat = float(request.args.get('Latitude'))
        long = float(request.args.get('Longitude'))
        #create dictionary
        to_predict_list = {'Latitude': lat, 'Longitude': long, 'Time': cdt}
        #run lat long checks, return message if they fail, else get pred
        response = run_constraints(to_predict_list, pdistrict_labenc, sdistrict_labenc, hood_labenc, inter_labenc, pdistrict_knn, sdistrict_lgbm, hood_knn, inter_knn)
        #return the result
        return jsonify(response)
    
# Start the server, continuously listen to requests.
if __name__=="__main__":
    # For local development, set to True:
    # app.run(debug=True)
    # For public web serving:
    app.run(host='97.113.5.182')
    app.run()
