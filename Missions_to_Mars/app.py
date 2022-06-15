from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# conn = 'mongodb://localhost:27017'
# client = PyMongo.MongoClient(conn)
# mars = client.mars_data
# mars.mars_data.drop()


# Route to render index.html template using data from Mongo
@app.route("/")
def home():
     # find one document from our mongo db and return it.
    mars = mongo.db.mars.find_one()
    # pass that listing to render_template
    return render_template('index.html', mars_data = mars)

# set our path to /scrape
@app.route("/scrape")
def scraper():
    # create a listings database
    mars = mongo.db.mars

    #  call the scrape function in scrape_mars file.
    mars_data = scrape_mars.scrape()
    
    # update database with the data that is being scraped.
    # mars.update({}, mars_data, upsert=True)
    mars.insert_one(mars_data)

    # return a message to our page so we know it was successful
    return redirect("/", code=302)

# Define Main Behavior
if __name__ == "__main__":
    app.run(debug=True)