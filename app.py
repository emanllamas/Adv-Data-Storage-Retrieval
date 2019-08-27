import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii copy.sqlite")

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
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/percipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tempature<br/>"
        f"<br/>"
        f"- start only calculates `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.<br/>"
        f"/api/v1.0/start<br/>"
        f"- When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.<br/>"
        f"/api/v1.0/start/end<br/>"
    
    
    )





@app.route("/api/v1.0/percipitation")
def percipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine) 
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    
    # Create a dictionary from the row data and append to a list of all_passengers
    date_prcp = []
    for date, prcp in results:
        date_prcp_dict = {}
        date_prcp_dict["date"] = date
        date_prcp_dict["Percipitation"] = prcp
        date_prcp.append(date_prcp_dict)

    return jsonify(date_prcp)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(Station.name).all()
    session.close()

    station_names = list(np.ravel(results))
    return jsonify(station_names)


@app.route("/api/v1.0/tempature")
def tempature():
    
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).all()
    session.close()

    tobs_dates = []
    tobs_dates_dict = {}
    for tobs, date in results:
        tobs_dates_dict["date"] = date
        tobs_dates_dict["tempature"] = tobs

        tobs_dates.append(tobs_dates_dict)
    
    return jsonify(tobs_dates)

@app.route("/api/v1.0/start/end")
def end():

    session = Session(engine)
    session.close()
    
    def calc_temps(start_date, end_date):

        return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    start_date = input(f'Enter start date in yyyy/mm/dd format')
    end_date = input(f'Enter end date in yyyy/mm/dd format')
   
    trip_temps = calc_temps(start_date, end_date)
    
    _min = trip_temps[0][0]
    _max = trip_temps[0][1]
    _avg = trip_temps[0][2]
    
    list_ = []
    list_.append(_max)
    list_.append(_min)
    list_.append(_avg)

    return jsonify(list_)


if __name__ == '__main__':
    app.run(debug=True, port=5009)
