
# Import Dependencies

import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#set up the database engine
engine = create_engine("sqlite:///hawaii.sqlite")

#reflect the database into our classes
Base = automap_base()

#reflect the tables
Base.prepare(engine, reflect=True)

#create variables for each of the classes
Measurement = Base.classes.measurement
Station = Base.classes.station

#create session link from python to database
#session = Session(engine)

#setup flask
app = Flask(__name__)

# 9.5.2 Create the Welcome Route
@app.route("/")

def welcome():
    return(
    '''
    Welcome to the Climate Analysis API! <br/>
    Available Routes: <br/>
    /api/v1.0/precipitation <br/>
    /api/v1.0/stations <br/>
    /api/v1.0/tobs <br/>
    /api/v1.0/temp/start/end <br/>
    ''')
  
#9.5.3 Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
   session = Session(engine)
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   session.close()
   return jsonify(precip)

# 9.5.4 Stations Route
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    session.close()
    return jsonify(stations=stations)

# 9.5.5 Monthly Temperature Route
@app.route("/api/v1.0/tobs")

def temp_monthly():
    session = Session(engine)
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    session.close()
    return jsonify(temps=temps)

    # 9.5.6 Statistics Route
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

#def stats():
 ##    return

def stats(start=None, end=None):
    session = Session(engine)
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
    session.close()
    return jsonify(temps)

def stats(start=dt.date(2017,6,1), end=dt.date(2017,6,30)):
    session = Session(engine)
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
    session.close()
    return jsonify(temps)    

if __name__ == '__main__':
    app.run()
