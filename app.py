# TODO show data when UPDATE
from flask import Flask, json, request, jsonify, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost/notes-api-rest-flask"
mongo = PyMongo(app)


@app.route("/notes", methods=["POST"])
def create_note():
    note_title = request.json["title"]
    note_description = request.json["description"]

    if note_title and note_description:

        note_id = mongo.db.notes.insert(
            {"title": note_title, "description": note_description}
        )

        response = {"id": str(note_id),
                    "title": note_title,
                    "description": note_description
                    }

        return response

    else:
        return not_found()


@app.route("/notes", methods=["GET"])
def get_notes():
    notes = mongo.db.notes.find()
    response = json_util.dumps(notes)

    return Response(response, mimetype="application/json")


@app.route("/notes/<id>", methods=["GET"])
def get_note(id):
    note = mongo.db.notes.find_one({"_id": ObjectId(id)})
    if note is not None:
        response = json_util.dumps(note)
    else:
        response = jsonify({"message": f"Id {id} is invalid!"})
        return response

    return Response(response, mimetype="application/json")


@app.route("/notes/<id>", methods=["DELETE"])
def delete_note(id):
    mongo.db.notes.delete_one({"_id": ObjectId(id)})
    response = jsonify({"message": f"Note {id} was deleted succesfully!"})

    return response


@app.route("/notes/<id>", methods=["PUT"])
def update_user(id):

    note_title = request.json["title"]
    note_description = request.json["description"]

    new_data = {
        "$set": {"title": note_title,
                 "description": note_description}

    }

    if note_title and note_description:
        mongo.db.notes.update_one({"_id": ObjectId(id)}, new_data)
        note = mongo.db.notes.find_one({"_id": ObjectId(id)})
        note_json = jsonify(json_util.dumps(note))
        message = jsonify({"message": f"Note {id} was updated succesfully!"})

        return message


@ app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        "message": "Resource Not Found " + request.url,
        "status": 404
    })
    response.status_code = 404
    return response


if __name__ == "__main__":
    app.run(debug=True)
