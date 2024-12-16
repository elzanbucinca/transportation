from flask import Blueprint, request, jsonify
from domain.person import Person
from domain.company import Company

customer = Blueprint('customer', __name__)

@customer.route("/private", methods = ['POST', 'PUT'])
def create_update_private():
    data = request.get_json()
    person = Person()
    person.from_dict_to_self(data)
    person.is_user = False

    match request.method:
        case "POST":
            person.add()
            return jsonify(person.to_dict()), 201
        case "PUT":
            person.update()
            return jsonify(person.to_dict()), 200


@customer.route("/private/<id>", methods = ['GET', 'DELETE'])
def get_delete_private(id):
    person = Person(id)
    
    match request.method:
        case "GET":
            person.find()
            return jsonify(person.to_dict()), 200
        case "DELETE":
            person.delete()
            return jsonify({"id": id}), 200
        
@customer.route("/corporate", methods = ['POST', 'PUT'])
def create_update_corporate():
    data = request.get_json()
    company = Company()
    company.from_dict_to_self(data)

    match request.method:
        case "POST":
            company.add()
            return jsonify(company.to_dict()), 201
        case "PUT":
            company.update()
            return jsonify(company.to_dict()), 200


@customer.route("/corporate/<id>", methods = ['GET', 'DELETE'])
def get_delete_corporate(id):
    company = Company(id)
    
    match request.method:
        case "GET":
            company.find()
            return jsonify(company.to_dict()), 200
        case "DELETE":
            company.delete()
            return jsonify({"id": id}), 200
