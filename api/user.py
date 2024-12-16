from flask import Blueprint, request, jsonify
from domain.person import Person

user = Blueprint('user', __name__)

@user.route("/", methods = ['POST', 'PUT'])
def create_update():
    data = request.get_json()
    person = Person()
    person.from_dict_to_self(data)
    person.is_user = True

    match request.method:
        case "POST":
            person.add()
            return jsonify(person.to_dict()), 201
        case "PUT":
            person.update()
            return jsonify(person.to_dict()), 200


@user.route("/<id>", methods = ['GET', 'DELETE'])
def get_delete(id):
    person = Person(id)
    
    match request.method:
        case "GET":
            person.find()
            return jsonify(person.to_dict()), 200
        case "DELETE":
            person.delete()
            return jsonify({"id": id}), 200
