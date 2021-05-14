from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost/notes-api-rest-flask"
mongo = PyMongo(app)


@app.route("/note", methods=["POST"])
def create_note():
    return {"note": "HOla mundo"}


if __name__ == "__main__":
    app.run(debug=True)
