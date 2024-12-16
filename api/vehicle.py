from flask import Blueprint, request, jsonify
from domain.bike import Bike
from domain.truck import Truck
from domain.ship import Ship
from domain.location import LocationList


vehicle = Blueprint('vehicle', __name__)

@vehicle.route("/<type>", methods = ['POST', 'PUT'])
def create_update(type):
    data = request.get_json()

    match type:
        case "bike":
            vehicle = Bike()
        case "ship":
            vehicle = Ship()
        case "truck":
            vehicle = Truck()
        case _:
            return {"error": f"Type {type} does not exist"}, 400

    vehicle.id = data['id']
    vehicle.current_position = LocationList().get_city_by_name(data['current_position'])

    match request.method:
        case "POST":
            vehicle.add()
            return jsonify(vehicle.to_dict()), 201
        case "PUT":
            vehicle.update()
            return jsonify(vehicle.to_dict()), 200


@vehicle.route("/<type>/<id>", methods = ['GET'])
def get(type, id):
    match type:
        case "bike":
            vehicle = Bike(id)
        case "ship":
            vehicle = Ship(id)
        case "truck":
            vehicle = Truck(id)
        case _:
            return {"error": f"Type {type} does not exist"}, 400

    match request.method:
        case "GET":
            vehicle.find()
            return jsonify(vehicle.to_dict()), 200
