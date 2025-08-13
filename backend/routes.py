from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    # This returns the contents of the data list in JSON format
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """
    Retrieve a single picture by its ID.
    ID in the URL is 1-based, but list indexes are 0-based.
    """
    # Ensure id is within range and data list is not empty
    if data and 1 <= id <= len(data):
        return jsonify(data[id - 1]), 200
    
    # Return a proper JSON error if not found
    return jsonify({"message": "Picture not found"}), 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture = request.get_json()  # Extract new picture from request body

    # Check if picture with this ID already exists in 'data'
    for item in data:
        if item.get('id') == picture.get('id'):
            # Duplicate found: return 302 with required message
            message = {"Message": f"picture with id {picture['id']} already present"}
            return jsonify(message), 302

    # No duplicate: add new picture
    data.append(picture)
    return jsonify(picture), 201  # Created

######################################################################
# UPDATE A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    new_picture = request.get_json()  # Extract updated picture data from request body

    # Find picture by id
    for idx, item in enumerate(data):
        if item.get('id') == id:
            # Update the item with new data
            data[idx] = new_picture
            return jsonify(new_picture), 200

    # If not found
    return jsonify({"message": "picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    # Find the picture by id in the data list
    for idx, item in enumerate(data):
        if item.get('id') == id:
            # Delete from the list
            del data[idx]
            return '', 204  # No content

    # Not found: return 404 with message
    return jsonify({"message": "picture not found"}), 404
