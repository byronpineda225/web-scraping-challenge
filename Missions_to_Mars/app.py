from flask import Flask, render_template, request, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

app.config['MONGO_URI'] = "mongodb://localhost:27017/mars_info"
mongo = PyMongo(app)

# Route to render index.html template using data from Mongo
@app.route("/")
def index():

    # Find one record of data from the mongo database
    mars_info = mongo.db.mars_info.find_one()

    # Return template and data
    return render_template("index.html", mars_info=mars_info)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_info = mongo.db.mars_info
    mars_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mars_info.update({}, mars_data, upsert=True)
    return redirect ("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)