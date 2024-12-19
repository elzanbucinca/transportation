from flask import Blueprint, request, jsonify
from domain.person import Person
from domain.company import Company

# Create a Flask Blueprint for customer-related routes
customer = Blueprint('customer', __name__)

@customer.route("/private", methods=['POST', 'PUT'])
def create_update_private():
    """
    Handles the creation or update of a private customer (individual).

    For POST requests:
        - Creates a new private customer using the provided JSON data.
        - Returns the created customer's data and a 201 status code.

    For PUT requests:
        - Updates an existing private customer's data using the JSON data.
        - Returns the updated customer's data and a 200 status code.

    Returns:
        Response: A JSON response containing the customer's data and the 
        HTTP status code.
    """
    # Extract JSON data from the request body
    data = request.get_json()

    # Initialize a Person object and populate it with the JSON data
    person = Person()
    person.from_dict_to_self(data)
    person.is_user = False  # Mark the person as a private customer

    # Handle the request method (POST or PUT)
    match request.method:
        case "POST":
            # Add a new private customer to the database
            person.add()
            return jsonify(person.to_dict()), 201  # Created
        case "PUT":
            # Update an existing private customer in the database
            person.update()
            return jsonify(person.to_dict()), 200  # OK


@customer.route("/private/<id>", methods=['GET', 'DELETE'])
def get_delete_private(id):
    """
    Handles retrieval or deletion of a private customer by ID.

    For GET requests:
        - Retrieves a private customer's data based on the provided ID.
        - Returns the customer's data and a 200 status code.

    For DELETE requests:
        - Deletes the private customer with the specified ID.
        - Returns the deleted customer's ID and a 200 status code.

    Args:
        id (str): The unique identifier of the private customer.

    Returns:
        Response: A JSON response containing the customer's data or ID and 
        the HTTP status code.
    """
    # Initialize a Person object with the given ID
    person = Person(id)

    # Handle the request method (GET or DELETE)
    match request.method:
        case "GET":
            # Find and return the customer's data
            person.find()
            return jsonify(person.to_dict()), 200  # OK
        case "DELETE":
            # Delete the customer and return their ID
            person.delete()
            return jsonify({"id": id}), 200  # OK


@customer.route("/corporate", methods=['POST', 'PUT'])
def create_update_corporate():
    """
    Handles the creation or update of a corporate customer (company).

    For POST requests:
        - Creates a new corporate customer using the provided JSON data.
        - Returns the created customer's data and a 201 status code.

    For PUT requests:
        - Updates an existing corporate customer's data using the JSON data.
        - Returns the updated customer's data and a 200 status code.

    Returns:
        Response: A JSON response containing the customer's data and the 
        HTTP status code.
    """
    # Extract JSON data from the request body
    data = request.get_json()

    # Initialize a Company object and populate it with the JSON data
    company = Company()
    company.from_dict_to_self(data)

    # Handle the request method (POST or PUT)
    match request.method:
        case "POST":
            # Add a new corporate customer to the database
            company.add()
            return jsonify(company.to_dict()), 201  # Created
        case "PUT":
            # Update an existing corporate customer in the database
            company.update()
            return jsonify(company.to_dict()), 200  # OK


@customer.route("/corporate/<id>", methods=['GET', 'DELETE'])
def get_delete_corporate(id):
    """
    Handles retrieval or deletion of a corporate customer by ID.

    For GET requests:
        - Retrieves a corporate customer's data based on the provided ID.
        - Returns the customer's data and a 200 status code.

    For DELETE requests:
        - Deletes the corporate customer with the specified ID.
        - Returns the deleted customer's ID and a 200 status code.

    Args:
        id (str): The unique identifier of the corporate customer.

    Returns:
        Response: A JSON response containing the customer's data or ID and 
        the HTTP status code.
    """
    # Initialize a Company object with the given ID
    company = Company(id)

    # Handle the request method (GET or DELETE)
    match request.method:
        case "GET":
            # Find and return the customer's data
            company.find()
            return jsonify(company.to_dict()), 200  # OK
        case "DELETE":
            # Delete the customer and return their ID
            company.delete()
            return jsonify({"id": id}), 200  # OK
