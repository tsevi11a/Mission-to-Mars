from flask import Flask, render_template, redirect, url_for #use flask to render a template
from flask_pymongo import PyMongo #use PyMongo to interact with mango db
import scraping #we'll use the scraping code

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app" # app will connect to mongo using a URI
mongo = PyMongo(app)

# Note: Flask routes bind URLs to functions
# Define route for HTML page
@app.route("/")
def index():
   mars = mongo.db.mars.find_one() #uses PyMongo to find the "mars" collection in our db
   return render_template("index.html", mars=mars) #tells Flask to return an HTML template using an index.html file

# Set up scraping route (will be the "button" that will scrape the updated data - i.e. will be tied to button that will run the code when clicked)
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars #points to our Mongo db
   mars_data = scraping.scrape_all() #variable to hold the newly scraped data -- references the scrape_all function in our scraping.py file
   mars.update({}, mars_data, upsert=True) #update the db, add empty JSON obj, data stored in mars_data, upsert-T indicates to Mongo to create new doc if one doesn't already exist
   return redirect('/', code=302) #navigates back to " / " where we can see the updated content

# Tell Flask to run
if __name__ == "__main__":
   app.run()