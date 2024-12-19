from flask import Blueprint, request, jsonify
from domain.bike import Bike
from domain.truck import Truck
from domain.ship import Ship
from domain.location import LocationList

# Create a Flask Blueprint for vehicle-related routes
vehicle = Blueprint('vehicle', __name__)

@vehicle.route("/<type>", methods=['POST', 'PUT'])
def create_update(type):
    """
    Handles the creation or update of a vehicle (bike, ship, or truck).

    For POST requests:
        - Creates a new vehicle of the specified type using the provided data.
        - Returns the created vehicle's data and a 201 status code.

    For PUT requests:
        - Updates an existing vehicle of the specified type using the data.
        - Returns the updated vehicle's data and a 200 status code.

    Args:
        type (str): The type of vehicle ('bike', 'ship', or 'truck').

    Returns:
        Response: A JSON response containing the vehicle's data and the 
        HTTP status code, or an error message with a 400 status code 
        if data is missing or the type is invalid.
    """
    # Extract JSON data from the request body
    data = request.get_json()

    # Validate required data fields
    if "id" not in data or "current_position" not in data:
        return jsonify({"error": "Missing data"}), 400

    # Determine the vehicle type and initialize the appropriate object
    match type:
        case "bike":
            vehicle = Bike()
        case "ship":
            vehicle = Ship()
        case "truck":
            vehicle = Truck()
        case _:
            # Return an error if the vehicle type is invalid
            return {"error": f"Type {type} does not exist"}, 400

    # Set the vehicle's ID and current position
    vehicle.id = data['id']
    vehicle.current_position = LocationList().get_city_by_name(
        data['current_position']
    )

    # Handle the request method (POST or PUT)
    match request.method:
        case "POST":
            # Add the new vehicle to the database
            vehicle.add()
            return jsonify(vehicle.to_dict()), 201  # Created
        case "PUT":
            # Update the existing vehicle in the database
            vehicle.update()
            return jsonify(vehicle.to_dict()), 200  # OK


@vehicle.route("/<type>/<id>", methods=['GET'])
def get(type, id):
    """
    Retrieves a vehicle of the specified type by its ID.

    For GET requests:
        - Finds a vehicle of the specified type using the provided ID.
        - Returns the vehicle's data and a 200 status code.

    Args:
        type (str): The type of vehicle ('bike', 'ship', or 'truck').
        id (str): The unique identifier of the vehicle.

    Returns:
        Response: A JSON response containing the vehicle's data and the 
        HTTP status code, or an error message with a 400 status code 
        if the type is invalid.
    """
    # Determine the vehicle type and initialize the appropriate object
    match type:
        case "bike":
            vehicle = Bike(id)
        case "ship":
            vehicle = Ship(id)
        case "truck":
            vehicle = Truck(id)
        case _:
            # Return an error if the vehicle type is invalid
            return {"error": f"Type {type} does not exist"}, 400

    # Handle the request method (GET)
    match request.method:
        case "GET":
            # Find the vehicle and return its data
            vehicle.find()
            return jsonify(vehicle.to_dict()), 200  # OK
