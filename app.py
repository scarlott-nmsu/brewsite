"""BrewSite Flask application.

Software Req Doc: Project 1 Flask app
Release Date: October 2026
Code Zack Scarlott
Description: Flask and Jinja website with a home page and a brewery page.
             The brewery page pulls live brewery data for Las Cruces, NM
             from the Open Brewery DB API.
"""

from flask import Flask, render_template, redirect, url_for   # web framework tools
import requests                                                # HTTP calls to the brewery API

app = Flask(__name__)   # create the Flask application object

# Open Brewery DB endpoint, filtered to Las Cruces, New Mexico
BREWERY_API = "https://api.openbrewerydb.org/v1/breweries"
API_PARAMS = {"by_city": "las_cruces", "by_state": "new_mexico", "per_page": 20}


def get_breweries():
    """Fetch breweries from the Open Brewery DB API.

    Returns:
        list: A list of brewery dictionaries, or an empty list if the
        request fails or times out.
    """
    try:
        response = requests.get(BREWERY_API, params=API_PARAMS, timeout=10)
        response.raise_for_status()       # raise an error on a 4xx or 5xx status
        return response.json()            # JSON list becomes a list of dictionaries
    except requests.RequestException:
        return []                         # page still loads if the API is down


@app.route("/")
def index():
    """Send the site root to the home page."""
    return redirect(url_for("home"))


@app.route("/home")
def home():
    """Render the home page."""
    return render_template("home.html", title="Home")


@app.route("/brewery")
def brewery():
    """Render the brewery page with live brewery data."""
    breweries = get_breweries()
    return render_template("brewery.html", title="Breweries", breweries=breweries)


# Start the development server only when this file is run directly
if __name__ == "__main__":
    app.run(debug=True)
