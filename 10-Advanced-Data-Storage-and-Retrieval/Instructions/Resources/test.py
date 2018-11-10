# Dependencies
import datetime as dt
from datetime import datetime, timedelta
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Setting up database

engine = create_engine('sqlite:///hawaii.sqlite')
Base = automap_base()
Base.prepare(engine, reflect=True)

# creating the refrence to the data base, when we use alchemy, this is what allows it to understand 

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

# Setting up flask

app = Flask(__name__)

# All of the routes the user can take along with an error message 
@app.route('/')
def home():
    return (
        f'Available Routes:<br/>'
        f'/api.v1.0/precip<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/date<br/>'
        f'/api/v1.0/start_date/end_date<br/>'
        f'** To prevent errors, please enter dates in "YYYY-MM-DD" format. **'
    )

# First route 

@app.route('/api.v1.0/precip')
def precip():

    # Query for the last year of percip data (had trouble getting the data from code so I just entered it manually)
    results_percp = session.query(Measurement.date,Measurement.prcp,Measurement.station).\
    filter(Measurement.date >= '2016-08-23').\
    order_by(Measurement.date).all()
    # putting results into a list so they can be jsonified. tried to use np.ravel but no success
    percp_list = [results_percp]
    # returning results
    return jsonify(percp_list)

# Next route 

@app.route('/api/v1.0/stations')
def stations():

    # query for the list of stations, their name, and elevation
    results_station = session.query(Station.station, Station.name, Station.elevation).all()

    station_list = [results_station]
    # returning results 
    return jsonify(station_list)

# Next route
@app.route('/api/v1.0/tobs')
def tobs():

    # query for temperature for the last year 
    tobs_result = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= '2016-08-23').all()

    tobs_list = [tobs_result]
    # returning results 
    return jsonify(tobs_list)

# Next route
@app.route('/api/v1.0/<date>')
def given_date(date):
    
    # query for avg, min, max temp data for a specific date
    date_results = session.query(Measurement.date, func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).\
        filter(Measurement.date == date).all()
    # when i first returned this data it was ugly and didnt make much sense so I am placing it in a dict 
    data_list = []
    for result in date_results:
        row = {'Date': result[0], 'Avg Temp:': result[1], 'Max Temp:':result[2], 'Min Temp:': result[3]}
        data_list.append(row)
    # returning results 
    return jsonify(data_list)

# final route
@app.route('/api/v1.0/<start_date>/<end_date>/')
def query_dates(start_date, end_date):
    # query for avg, min, max, temp data between specific dates 
    results = session.query(func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).\
        filter(Measurement.date >= start_date, Measurement.date <= end_date).all()
    # again, using a dict to fix the format of the result 
    data_list = []
    for result in results:
        row = {'Start Date': start_date, 'End Date': end_date, 'Avg Temp:': result[0], 'Max Temp:':result[1], 'Min Temp:': result[2]}
        data_list.append(row)
    # returning result 
    return jsonify(data_list)

# debug statement 
if __name__ == '__main__':
    app.run(debug=True)