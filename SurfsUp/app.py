## Part 2: Design Your Climate App

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
        f"<h1>Hello! Welcome to my API.</h1>"
        f"<h2>The available routes are:</h2>"
        f"<h3>/api/v1.0/precipitation<br/>"
        f"To see the last 12 months of precipitation data.</h3>"
        f"<h3>/api/v1.0/stations<br/>"
        f"To see a list of all stations.</h3>"        
        f"<h3>/api/v1.0/tobs<br/>"
        f"To see the last 12 months of temperature observations for the most active station.</h3>"
        f"<h3>/api/v1.0/YYYY-MM-DD<br/>"
        f"To see the minimum, maximum and average temperatures calculated from the given start date to the end of the dataset.</h3>"
        f"<h3>/api/v1.0/YYYY-MM-DD/YYYY-MM-DD<br/>"
        f"To see the minimum, maximum and average temperatures calculated from the given start and end date.</h3>"        
        f"Note: Data available between 2010-01-01 and 2017-08-23"
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

    # Close session
    session.close() 

    # Convert list to a dictionary with the date as Key and prcp as a list of values
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

    # Close session
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

    # Close session
    session.close()

    # Convert into a list of lists
    tobs_list = [[x[0],x[1]] for x in tobs]

    # Return JSON representation of list
    return jsonify(tobs_list)

#################################################
### API Dynamic Route
#################################################

# <start> route
@app.route("/api/v1.0/<start>")
def start(start):
    """Minimum, maximum and average temperatures calculated from a given start date until the end of the dataset."""

    # Create session from Python to the DB
    session = Session(engine)

    # Find the most recent date in the data set
    last_date = session.query(func.max(M.date)).scalar()

    # Find the first date in the data set
    first_date = session.query(func.min(M.date)).scalar()

    # Check if start date exists in data base
    if start >=first_date and start <= last_date:

        # Query minimum, maximum and average temperature for a specified start date
        temperatures = session.query(func.min(M.tobs), func.max(M.tobs), func.avg(M.tobs)) \
                        .filter(M.date >= start).all()

        # Close session
        session.close()

        # Convert into a list
        temperatures_list = [[x[0],x[1],x[2]] for x in temperatures]

        # Return JSON representation of list
        return jsonify(temperatures_list)
    
    # Error message in case start date is not present in the dataset
    return jsonify({"error": f"{start} is not present in the dataset."}), 404

# /api/v1.0/<start>/<end> route
@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    """Minimum, maximum and average temperatures calculated from the given start and end date."""

    # Create session from Python to the DB
    session = Session(engine)

    # Find the most recent date in the data set
    last_date = session.query(func.max(M.date)).scalar()

    # Find the first date in the data set
    first_date = session.query(func.min(M.date)).scalar()

    # Check if start date is after end date
    if end<start:

        # Error message in case start date is after end date
        return jsonify({"error": f"start date cannot be after end date."}), 404        
    
    # Check if start date does not exist in data base
    elif start < first_date or start > last_date:
        if end >= first_date and end <= last_date:

            # Error message in case start date is not present in the dataset
            return jsonify({"error": f"{start} is not present in the dataset."}), 404    
    
        else:
        # Error message in case start and end dates are not present in the dataset
            return jsonify({"error": f"{start} and {end} are not present in the dataset."}), 404        

    # Check if end date does not exist in data base    
    elif end < first_date or end > last_date:

        # Error message in case end date is not present in the dataset
        return jsonify({"error": f"{end} is not present in the dataset."}), 404    

    else:
        # Query minimum, maximum and average temperature for a specified start date
        temperatures = session.query(func.min(M.tobs), func.max(M.tobs), func.avg(M.tobs)) \
                        .filter(M.date >= start, M.date <= end).all()

        # Close session
        session.close()

        # Convert into a list
        temperatures_list = [[x[0],x[1],x[2]] for x in temperatures]

        # Return JSON representation of list
        return jsonify(temperatures_list)

if __name__ == "__main__":
    app.run(debug=True)