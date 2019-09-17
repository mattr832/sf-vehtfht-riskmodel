from flask import Flask
from flask_sqlalchemy import SQLAlchemy
 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///riskmodel.db'
app.secret_key = "MATmani8"
 
db = SQLAlchemy(app)