# sqlalchemy-challenge

Congratulations! You've decided to treat yourself to a long holiday vacation in Honolulu, Hawaii. To help with your trip planning, you decide to do a climate analysis about the area. The following sections outline the steps that you need to take to accomplish this task.

## Part 1: Analyze and Explore the Climate Data

### Precipitation Analysis

- Most recent date in the dataset.

![](Pics/1.png)

- Date one year from the last date in data set.

![](Pics/2.png)

- Pandas DataFrame with 12 months of precipitation data

![](Pics/3.png)

- Line chart with the results

![](Pics/4.png)

- Print the summary statistics for the precipitation data.

![](Pics/5.png)

### Station Analysis

    Design a query to calculate the total number of stations in the dataset.

    Design a query to find the most-active stations (that is, the stations that have the most rows). To do so, complete the following steps:

        List the stations and observation counts in descending order.
    hint

    You’ll need to use the func.count function in your query.
        Answer the following question: which station id has the greatest number of observations?

    Design a query that calculates the lowest, highest, and average temperatures that filters on the most-active station id found in the previous query.
    hint

    You’ll need to use functions such as func.min, func.max, and func.avg in your query.

    Design a query to get the previous 12 months of temperature observation (TOBS) data. To do so, complete the following steps:

        Filter by the station that has the greatest number of observations.

        Query the previous 12 months of TOBS data for that station.

        Plot the results as a histogram with bins=12, as the following image shows:

        A screenshot depicts the histogram.

    Close your session.

Part 2: Design Your Climate App

Now that you’ve completed your initial analysis, you’ll design a Flask API based on the queries that you just developed. To do so, use Flask to create your routes as follows:

    /

        Start at the homepage.

        List all the available routes.

    /api/v1.0/precipitation

        Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.

        Return the JSON representation of your dictionary.

    /api/v1.0/stations
        Return a JSON list of stations from the dataset.

    /api/v1.0/tobs

        Query the dates and temperature observations of the most-active station for the previous year of data.

        Return a JSON list of temperature observations for the previous year.

    /api/v1.0/<start> and /api/v1.0/<start>/<end>

        Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.

        For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.

        For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.

Hints

    Join the station and measurement tables for some of the queries.

    Use the Flask jsonify function to convert your API data to a valid JSON response object.

