## Part 2: Design Your Climate App

# Imports
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Flask
from flask import Flask, jsonify


#################################################
### API SQLite Connection & Landing Page
#################################################

# Create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
base = automap_base()

# Reflect the tables
base.prepare(autoload_with=engine)

# Save references to each table
S = base.classes.station
M = base.classes.measurement

# Flask Setup
app = Flask(__name__)

# Landing Page
@app.route("/")
def landing():
    """List all available api routes."""

    # Display available routes
    return (
        f"Hello, the available routes are:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )

#################################################
### API Static Routes
#################################################

# Precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Last 12 months of precipitation data."""

    # Create session from Python to the DB
    session = Session(engine)

    # Find the most recent date in the data set
    most_recent = session.query(func.max(M.date)).scalar()
    
    # Calculate the date one year before the most recent date in the data set
    one_year = session.query(func.date(most_recent, "-1 year")).scalar()
    
    # Create a query to retrieve the last 12 months of precipitation data
    precip = session.query(M.date, M.prcp).filter(M.date.between(one_year, most_recent)).all()

    # Close Session
    session.close() 

    # Convert list to a dictionary
    precip_dict = {}
    for date, prcp in precip:
        if date in precip_dict:
            precip_dict[date].append(prcp)
        else:
            precip_dict[date] = [prcp]

    # Return JSON representation of dictionary
    return jsonify(precip_dict)

# stations route
@app.route("/api/v1.0/stations")
def stations():
    """List of all stations."""
    
    # Create session from Python to the DB
    session = Session(engine)

    # Create a query to retrieve the list of stations
    stations = session.query(S.station).all()

    # Close Session
    session.close() 

    # Convert into a list
    stations_list = [x[0] for x in stations]

    # Return JSON representation of list
    return jsonify(stations_list)

# TOBS route
@app.route("/api/v1.0/tobs")
def tobs():
    """Last 12 months of temperature observations for the most active station."""

    # Create session from Python to the DB
    session = Session(engine)

    # Find the most active station
    active_station = session.query(M.station).group_by(M.station).order_by(func.count(M.station).desc()).first()

    # Find the most recent date in the data set
    most_recent = session.query(func.max(M.date)).scalar()
    
    # Calculate the date one year before the most recent date in the data set
    one_year = session.query(func.date(most_recent, "-1 year")).scalar()

    # Create a query to retrieve the last 12 months of temperature observations for the most active station
    tobs = session.query(M.date, M.tobs).filter(M.station == active_station[0], \
                                M.date.between(one_year, most_recent)).all()

    # Close Session
    session.close()

    # Convert into a list of lists
    tobs_list = [x[0] for x in tobs]

    return jsonify(tobs_list)


# /api/v1.0/<start>
# /api/v1.0/<start>/<end>

#################################################
# Flask Routes
#################################################
### API Static Routes

### API Dynamic Route

if __name__ == "__main__":
    app.run(debug=True)