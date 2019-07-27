
#import dependencies
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func,inspect,and_,distinct,desc

#give the path
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

# 1. import Flask
from flask import Flask, jsonify

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

@app.route("/")
def home():
    return (f"Welcome!!: Climate API for Hawaii<br/>"
            f"Available Routes:<br/>"
            f"/api/v1.0/precipitation --- a list of all precipitation date<br/>"
            f"/api/v1.0/stations ---- a list of stations<br/>"
            f"/api/v1.0/tobs ---  latest year of temperature data<br/>"
            f"/api/v1.0/yyyy-mm-dd ---  latest temperature data from user provided start date,enter date in %Y-%m-%d format <br/>"
            f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd ---  temperature data for a given start-end date pair,enter start date followed by end date in %Y-%m-%d format <br/>"
            f"------------------------------------")
            
            
            
            
@app.route("/api/v1.0/precipitation")
def precipitation_data():
       recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
       #date_1 = list(np.ravel(recent_date))[0]
       date_1 = recent_date[0]
       date_2 = dt.datetime.strptime(date_1, "%Y-%m-%d")
       year_ago =date_2 - dt.timedelta(days=365)
       qry = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >=year_ago.date()).all()
       
       dict_prcp = dict(qry)
    
       return jsonify(dict_prcp)
    
    
@app.route("/api/v1.0/stations")
def station_data():
    station_data = session.query(Station.station,Station.name,Station.latitude,Station.longitude).all()
    return jsonify(station_data)


@app.route("/api/v1.0/tobs")
def tobs_data():
       recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
       #date_1 = list(np.ravel(recent_date))[0]
       date_1 = recent_date[0]
       date_2 = dt.datetime.strptime(date_1, "%Y-%m-%d")
       year_ago =date_2 - dt.timedelta(days=365)
       qry_tobs = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date >=year_ago.date()).all()
       
       return jsonify(qry_tobs)


@app.route("/api/v1.0/<start>")
def tobs_data_start(start):
       start_date = dt.datetime.strptime(start, "%Y-%m-%d")
       
       qry_tobs = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
       filter(Measurement.date >= start_date.date()).all()
    
       return jsonify(qry_tobs)

@app.route("/api/v1.0/<start>/<end>")
def tobs_data_start_end(start,end):
       start_date = dt.datetime.strptime(start, "%Y-%m-%d")
       end_date = dt.datetime.strptime(end, "%Y-%m-%d")
       #qry_tobs = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date >= start_date.date()).all()
       
       qry_tobs_start_end = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
       filter(Measurement.date >= start_date.date()).filter(Measurement.date <= end_date.date()).all()
    
       return jsonify(qry_tobs_start_end)
    
if __name__ == "__main__":
    app.run(debug=True)
    
    
      







