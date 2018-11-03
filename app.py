import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate API!<br/>"
        f"<br/>"
        f"Available Routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"/api/v1.0/start<br/>"
        f"<br/>"
        f"/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Dictionary of total rainfall
    date_one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    rain = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > date_one_year_ago).order_by(Measurement.date).all()
    total_rain = []
    for result in rain:
        row = {}
        row[result[0]] = result[1]
        total_rain.append(row)
    
    """Return the total rainfall data as json"""
    return jsonify(total_rain)

@app.route("/api/v1.0/stations")
def stations():
    stations_query = session.query(Station.name, Station.station)
    stations = pd.read_sql(stations_query.statement, stations_query.session.bind)
    return jsonify(stations.to_dict())

@app.route("/api/v1.0/tobs")
def tobs():
    # Dictionary of total temperature observations
    date_one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    temperature_observations = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > date_one_year_ago).order_by(Measurement.date).all()
    total_temperature = []
    for result in temperature_observations:
        row = {}
        row["date"] = result[0]
        row["tobs"] = result[1]
        total_temperature.append(row)
    
    """Return the total rainfall data as json"""
    return jsonify(total_temperature)

@app.route("/api/v1.0/<start>")
def trip_1(start):
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    start = dt.date(2016, 8, 24) - dt.timedelta(days=365)
    end =  dt.date(2017, 8, 23)
    trip_data = session.query(func.min(Measurement.tobs), func.round(func.avg(Measurement.tobs), 1), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return jsonify(trip_data)

@app.route("/api/v1.0/<start>/<end>")
def trip_2(start,end):
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
    start = dt.date(2016, 8, 24) - dt.timedelta(days=365)
    end =  dt.date(2016, 9, 7) - dt.timedelta(days=365)
    trip_data = session.query(func.min(Measurement.tobs), func.round(func.avg(Measurement.tobs), 1), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return jsonify(trip_data)



if __name__ == "__main__":
    app.run(debug=True)