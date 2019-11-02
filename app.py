import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
# /

# Home page.

# List all routes that are available.

# /api/v1.0/precipitation

# Convert the query results to a Dictionary using date as the key and prcp as the value.

# Return the JSON representation of your dictionary.

# /api/v1.0/stations

# Return a JSON list of stations from the dataset.
# /api/v1.0/tobs

# query for the dates and temperature observations from a year from the last data point.
# Return a JSON list of Temperature Observations (tobs) for the previous year.
# /api/v1.0/<start> and /api/v1.0/<start>/<end>

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.

# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date<br/>"
        f"Enter the date as yyyy-mm-dd"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=366)
    query_2=session.query(Measurement.date,Measurement.prcp).\
    filter(Measurement.date >query_date).all()


    session.close()

    # Convert list of tuples into normal list
    #all_names = list(np.ravel(results))
    all_precipation=[]
    for date,prcp in query_2:
        precipation_dict = {}
        precipation_dict[date] = prcp
        all_precipation.append(precipation_dict)

    return jsonify(all_precipation)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    query_station=session.query(Measurement.station).group_by(Measurement.station).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_stations = list(np.ravel(query_station))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=366)
    query_temp=session.query(Measurement.date,Measurement.tobs).\
    filter(Measurement.date >query_date).all()

    session.close()

    # Convert list of tuples into normal list
    all_temp=[]
    for _,temp in query_temp:
        all_temp.append(temp)

    

    return jsonify(all_temp)

@app.route("/api/v1.0/<starting_date>")
def n1(starting_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    	filter(Measurement.date >= starting_date).all()
    	 
        
    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)

@app.route("/api/v1.0/<start_date>/<end_date>")
def n2(start_date,end_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    	filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)

if __name__ == '__main__':
    app.run(debug=True)
