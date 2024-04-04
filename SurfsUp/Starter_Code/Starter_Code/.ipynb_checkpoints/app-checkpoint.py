# Import the dependencies.
import numpy as np
import pandas as pd
import sqlalchemy
import datetime as dt
import re
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# Declare a Base using `automap_base()`
Base = automap_base()
# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

#1
@app.route("/")
def welcome():
    return (
        f"Welcome to the SQL-Alchemy APP API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]/[end_date format:yyyy-mm-dd]<br/>"
    )

#2
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    recent_year= dt.date(2017, 8, 23)-dt.timedelta(days=365)
    last_date = dt.date(recent_year.year, recent_year.month, recent_year.day)
    query= session.query(measurement.date, measurement.prcp).filter(measurement.date >= last_date).order_by(measurement.date).all()
    prcp_dict = dict(query)

    print(f"Precipitation Results - {prcp_dict}")
    print("Out of Precipitation section.")
    return jsonify(prcp_dict) 


    prcp_dates = []
    prcp_totals = []

    for date, dailytotal in precipitation:
        prcp_dates.append(date)
        prcp_totals.append(dailytotal)
    
        prcp_dict = dict(zip(prcp_dates, prcp_totals))

    return jsonify(prcp_dict)

#3
@app.route("/api/v1.0/stations")
def stations():
    stations_query = session.query(Station.name, Station.station)
    stations = pd.read_sql(stations_query.statement, stations_query.session.bind)
    return jsonify(stations.to_dict())

#4
def tobs():
    session = Session(engine)
    queryresult = session.query( Measurement.date, Measurement.tobs).filter(Measurement.station=='USC00519281')\
         .filter(Measurement.date>='2016-08-23').all()

    tob = []
    for date, tobs in queryresult:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Tobs"] = tobs
        tob_obs.append(tobs_dict)
    return jsonify(tob)

#5 start
@app.route("/api/v1.0/<start>")

def temps_start(start):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
              filter(Measurement.date >= start).all()
    session.close()

    tobs_values = []
    for min, avg, max in results:
        tobs_dict = {}
        tobs_dict["min_temp"] = min
        tobs_dict["avg_temp"] = avg
        tobs_dict["max_temp"] = max
        tobs.append(tobs_dict) 
    return jsonify(tobs_values)

#5 end
@app.route("/api/v1.0/<start>/<end>")
def temps_end(start, end):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
              filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()

    tobs_values = []
    for min, avg, max in results:
        tobs_dict = {}
        tobs_dict["min_temp"] = min
        tobs_dict["avg_temp"] = avg
        tobs_dict["max_temp"] = max
        tobs.append(tobs_dict) 
    return jsonify(tobs_values)

if __name__ == "__main__":
    app.run(debug=True)
