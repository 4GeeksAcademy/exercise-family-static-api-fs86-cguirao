"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

from flask import jsonify


@app.route('/members', methods=['GET'])
def member_list():
    try:
        members = jackson_family.get_all_members()
        if not members:
            return jsonify({"error": "No members found"}), 400

        response_body = {
            "family": members
        }
        return jsonify(response_body), 200

    except Exception as e:  
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    try:
        member = jackson_family.get_member(id)

     
        if member is None:
            return jsonify({'error': 'Member not found'}), 400

      
        response_body = {
            "id": member["id"], 
            "first_name": member["first_name"],  
            "age": member["age"], 
            "lucky_numbers": member["lucky_numbers"] 
        }
        return jsonify(response_body), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/member', methods=['POST'])
def add_member():
    try:
        member_data = request.get_json()

        if not all(key in member_data for key in ( "first_name", "age", "lucky_numbers")):
            return jsonify({"error": "Missing required fields"}), 400

        jackson_family.add_member(member_data)
        return jsonify({"message": "Member added successfully"}), 200

    except Exception as e: 
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    try:
        result = jackson_family.delete_member(member_id)

        if result==False:
            return jsonify({"error": "Member not found"}), 400

        return jsonify({"done": True}), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    
   
    jackson_family = FamilyStructure("Jackson")
    
  
    jackson_family.add_member({
        "first_name": "John Jackson",
        "age": 33,
        "lucky_numbers": [7, 13, 22]
    })

    jackson_family.add_member({
        "first_name": "Jane Jackson",
        "age": 35,
        "lucky_numbers": [10, 14, 3]
    })

    jackson_family.add_member({
        "first_name": "Jimmy Jackson",
        "age": 5,
        "lucky_numbers": [1]
    })

    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
