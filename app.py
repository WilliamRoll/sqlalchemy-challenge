import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
#Measurement table
measurement =  Base.classes.measurement
#Station Table
station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start_end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def measurements():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    last_date = dt.date(2017,8,23)

    #locate and define 12 month date
    twelve_months = last_date - dt.timedelta(weeks=52)

    #prcp and date
    prcp = [measurement.date,
        func.avg(measurement.prcp)]

    #12 month of precp query data
    prcp_twelve_mon = session.query(*prcp).\
        filter(measurement.date >= twelve_months).\
        group_by(measurement.date).\
        order_by(measurement.date).all()

    session.close()

    #dictionary
    prcp_data = []
    for date, prcp in prcp_twelve_mon:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_data.append(prcp_dict)

    return jsonify(prcp_data)

@app.route("/api/v1.0/stations")
def station_names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #query for all station names
    station_name = session.query(station.station).\
        order_by(station.station).all()

    session.close()

    #dictionary
    station_data = []
    for stat in station_name:
        stat_dict = {}
        stat_dict["station"] = stat    
        station_data.append(stat_dict)

    return jsonify(station_data) 

@app.route("/api/v1.0/tobs")
def most_active():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    last_date = dt.date(2017,8,23)

    #locate and define 12 month date
    twelve_months = last_date - dt.timedelta(weeks=52)

    #query
    temps_ma = session.query(measurement.date, measurement.tobs).\
        filter(measurement.date >= twelve_months, measurement.station == 'USC00519281').all()

    session.close()

    #dictionary
    temp_data = []
    for date, tobs in temps_ma:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["tobs"] = tobs   
        temp_data.append(temp_dict) 

    return jsonify(temp_data)
    
@app.route("/api/v1.0/start")
def start_only():
    user_start_date = input("Please input start date 'YYYY-MM-DD': ")

    # Create our session (link) from Python to the DB
    session = Session(engine)

    #functions
    sel = [measurement.date, func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]

    #query
    station_sum_stats = session.query(*sel).\
        filter(measurement.date >= user_start_date).\
        group_by(measurement.date).\
        order_by(measurement.date).all()

    session.close()

    #dictionary
    sum_stats_data = []
    for date, min_tobs, avg_tobs, max_tobs in station_sum_stats:
        sum_stats_dict = {}
        sum_stats_dict["date"] = date
        sum_stats_dict["min temp"] = min_tobs
        sum_stats_dict["avg temp"] = avg_tobs
        sum_stats_dict["max temp"] = max_tobs  
        
        sum_stats_data.append(sum_stats_dict) 

    return jsonify(sum_stats_data)

@app.route("/api/v1.0/start_end")
def start_end():
    user_start_date = input("Please input start date 'YYYY-MM-DD': ")
    user_end_date = input("Please input end date 'YYYY-MM-DD': ")

    # Create our session (link) from Python to the DB
    session = Session(engine)

    #functions
    sel = [measurement.date, func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]

    #query
    station_sum_stats_se = session.query(*sel).\
        filter(measurement.date >= user_start_date, measurement.date <= user_end_date).\
        group_by(measurement.date).\
        order_by(measurement.date).all()

    session.close()

    #dictionary
    sum_stats_data_se = []
    for date, min_tobs, avg_tobs, max_tobs in station_sum_stats_se:
        sum_stats_dict_se = {}
        sum_stats_dict_se["date"] = date
        sum_stats_dict_se["min temp"] = min_tobs
        sum_stats_dict_se["avg temp"] = avg_tobs
        sum_stats_dict_se["max temp"] = max_tobs  
        
        sum_stats_data_se.append(sum_stats_dict_se) 

    return jsonify(sum_stats_data_se) 

if __name__ == '__main__':
    app.run(debug=True)
