#importing libraries
import flask
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
# from dbapp import app, Response
# from db_setup import init_db, db_session
# from datamodel import Response
from sf_vehthft_utils import *
from sf_vehthft_getmap import *


#initialize the database
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///riskmodel.db'
app.secret_key = "MATmani8"
 
db = SQLAlchemy(app)

class Response(db.Model):
    __tablename__ = "responses"
 
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.String)
    riskscore = db.Column(db.Integer)
    risklevel = db.Column(db.String)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
 
    def __repr__(self):
        return "<Response: {}>".format(self.name)

db.create_all()
db.session.commit()

# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
 
# engine = create_engine('sqlite:///riskmodel.db', convert_unicode=True)
# db_session = scoped_session(sessionmaker(autocommit=False,
#                                          autoflush=False,
#                                          bind=engine))
# Base = declarative_base()
# Base.query = db_session.query_property()
 
# Base.metadata.create_all(bind=engine)

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
        #add data to the database
        datafordb = Response(datetime = response['DateTime'],
                             riskscore = response['Risk Score'],
                             risklevel = response['Risk Level'],
                             latitude = response['Latitude'],
                             longitude = response['Longitude'])
        db.session.add(datafordb)
        db.session.commit()
        #get map with marker html and save into the templates folder
        get_map(response)
        #return the result
        return render_template("result.html", response=response)
    
# Start the server, continuously listen to requests.
if __name__=="__main__":
    # For local development, set to True:
    # app.run(debug=True)
    # For public web serving:
    app.run(host='97.113.5.182')
    app.run()
