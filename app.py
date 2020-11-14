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
Station = Base.classes.station

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
        # f"/api/v1.0/stations<br/>"
        # f"/api/v1.0/tobs<br/>"
        # f"/api/v1.0/tobs<br/>"
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

    # Create a dictionary from the row data and append to a list
    prcp_data = []
    for date, prcp in prcp_twelve_mon:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_data.append(prcp_dict)

    return jsonify(prcp_data)


if __name__ == '__main__':
    app.run(debug=True)
