# Import dependencies
import datetime as dt
import numpy as np
import pandas as pd


# Import SQLAlchemy dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Import flask.
from flask import Flask,jsonify

# reflect an existing database into a new model
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect the tables
Base = automap_base()

# We can view all of the classes that automap found
Base.prepare(engine, reflect=True)

# Save references to each table
# We can give classes new variable names
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
# We'll use an SQLAlchemy Session to query our database. 
# Our session essentially allows us to query for data.
session = Session(engine)

# Set up Flask
# Create a new Flask app instance (singular version of something)
app = Flask(__name__)

# Create a welcome route
@app.route('/')
def welcome():
    return(
    '''
    Welcome to the Hawaii Climate Analysis API!
    f"Available Routes:<br/>
       /api/v1.0/precipitation<br/>
       /api/v1.0/stations<br/>
       /api/v1.0/tobs<br/>
       /api/v1.0/temp/start/end
    ''')

# Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

# Stations Route
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# Monthly Temperature Route
@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# Statistics Route
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

if __name__ == '__main__':
     app.run()

