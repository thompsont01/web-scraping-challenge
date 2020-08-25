from flask import Flask, render_template, request, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)

app.config['MONGO_URI'] = "mongodb://localhost:27017/data"
mongo = PyMongo(app)

@app.route("/")
def homepage():
    data = mongo.db.collection.find_one()
    return render_template("index.html", data = data)

@app.route("/scrape")
def scrape():
    data = scrape_mars.scrape()

    mongo.db.collection.update({}, data, upsert = True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug = True)
