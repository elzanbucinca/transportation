from flask import Blueprint, request, jsonify
from domain.person import Person

# Create a Flask Blueprint for user-related routes
user = Blueprint('user', __name__)

@user.route("/", methods=['POST', 'PUT'])
def create_update():
    """
    Handles the creation or update of a user.

    For POST requests:
        - Creates a new user using the provided JSON data.
        - Returns the created user's data and a 201 status code.

    For PUT requests:
        - Updates an existing user's data using the provided JSON data.
        - Returns the updated user's data and a 200 status code.

    Returns:
        Response: A JSON response containing the user's data and the HTTP 
        status code.
    """
    # Extract JSON data from the request body
    data = request.get_json()
    
    # Initialize a Person object and populate it with the JSON data
    person = Person()
    person.from_dict_to_self(data)
    person.is_user = True  # Mark the person as a user

    # Handle the request method (POST or PUT)
    match request.method:
        case "POST":
            # Add a new user to the database
            person.add()
            return jsonify(person.to_dict()), 201  # Created
        case "PUT":
            # Update an existing user in the database
            person.update()
            return jsonify(person.to_dict()), 200  # OK


@user.route("/<id>", methods=['GET', 'DELETE'])
def get_delete(id):
    """
    Handles retrieval or deletion of a user by ID.

    For GET requests:
        - Retrieves a user's data based on the provided ID.
        - Returns the user's data and a 200 status code.

    For DELETE requests:
        - Deletes the user with the specified ID.
        - Returns the deleted user's ID and a 200 status code.

    Args:
        id (str): The unique identifier of the user.

    Returns:
        Response: A JSON response containing the user's data or ID and the 
        HTTP status code.
    """
    # Initialize a Person object with the given ID
    person = Person(id)

    # Handle the request method (GET or DELETE)
    match request.method:
        case "GET":
            # Find and return the user's data
            person.find()
            return jsonify(person.to_dict()), 200  # OK
        case "DELETE":
            # Delete the user and return their ID
            person.delete()
            return jsonify({"id": id}), 200  # OK
