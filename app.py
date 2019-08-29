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
engine = create_engine("sqlite:///hawaii.sqlite")

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
#################################################

@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/percipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tempature<br/>"
        f"/api/v1.0/start_end/<start_date>/<end_date><br/>"
        f"Enter start_date and <end_date> in YYYY-MM-DD format"
    )





@app.route("/api/v1.0/percipitation")
def percipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine) 
    results = session.query(Measurement.date, Measurement.prcp).limit(250)
    session.close()
    
    prcp_date = []
    prcp_date_dict = {}
    for date, prcp in results:
        prcp_date_dict['Date'] = date
        prcp_date_dict['Prcp'] = prcp
        prcp_date.append(prcp_date_dict)
    
    return jsonify(prcp_date)




@app.route("/api/v1.0/stations")
def stations():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    results = session.query(Station.station, Station.name).all()
    session.close()

    station_name = []
    for station, name in results:
        station_name_dict = {}
        station_name_dict['Station'] = station
        station_name_dict['Name'] = name
        station_name.append(station_name_dict)
    
    return jsonify(station_name)


@app.route("/api/v1.0/tempature")
def tempature():
        
    date = dt.date(2016,7,23) 

    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date > date).all()
    session.close()


    tobs_dates = []
    for date, tobs in results:
        tobs_dates_dict = {}
        tobs_dates_dict["date"] = date
        tobs_dates_dict["tempature"] = tobs

        tobs_dates.append(tobs_dates_dict)
    
    return jsonify(tobs_dates)

@app.route("/api/v1.0/start_end/<start_date>/<end_date>")
def start_end(start_date, end_date):

    date1 = start_date
    svalues = date1.split("-")
    syear = int(svalues[0])
    smonth = int(svalues[1])
    sday = int(svalues[2])

    date2 = end_date
    evalues = date2.split("-")
    eyear = int(evalues[0])
    emonth = int(evalues[1])
    eday = int(evalues[2])


    start_date1 = dt.date(syear,smonth,sday)
    end_date1 = dt.date(eyear,emonth,eday)
    
    def calc_temps(start_date, end_date):

        session = Session(engine)

        return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

        session.close()

    results1 = calc_temps(start_date1, end_date1)
    
    return jsonify({'Min':results1[0][0], 'Avg':results1[0][1], 'Max':results1[0][2]})


if __name__ == '__main__':
    app.run(debug=True, port=5009)
