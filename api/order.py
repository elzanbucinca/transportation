from flask import Blueprint, request, jsonify
import uuid
from datetime import datetime
from domain.order import Order, OrderStatus
from domain.vehicle import Vehicle

# Create a Flask Blueprint for order-related routes
order = Blueprint('order', __name__)

def from_data_to_order(data: dict):
    """
    Converts raw data into an Order object by initializing and setting its properties.

    Args:
        data (dict): A dictionary containing order details, such as items, weights, 
        and other relevant fields.

    Returns:
        Order: A fully initialized Order object with total weight, order ID, 
        vehicle assignment, and status set.

    Note:
        This function assigns the first available vehicle based on the number of items 
        and total weight of the order.
    """
    # Generate a unique order ID (first 4 characters of a UUID)
    data["id"] = str(uuid.uuid4())[:4]
    data["total_weight"] = 0  # Initialize total weight
    data["vehicle_id"] = ""  # Initialize vehicle assignment
    data["order_status"] = OrderStatus.PROCESSING.value  # Set initial status
    data["order_date"] = datetime.today().strftime("%Y%m%d")  # Current date

    # Initialize the Order object
    order = Order()
    order.from_dict_to_self(data)
    
    # Calculate total weight of all items in the order
    order.total_weight = round(sum([item.weight for item in order.items]), 2)
    
    # Assign the first available vehicle based on items and weight
    # Comment the following line to test shipment scenarios below.
    order.vehicle = Vehicle().get_first_available(len(order.items), order.total_weight)


    #### TESTS ####
    # Uncomment the following lines to test shipment scenarios.
    # order.vehicle = Vehicle().get_first_available(1, 5) # Shipment1 Test
    # order.vehicle = Vehicle().get_first_available(12, 3) # Shipment2 Test
    # order.vehicle = Vehicle().get_first_available(60, 4500) # Shipment3 Test
    # order.vehicle = Vehicle().get_first_available(120, 2500) # Shipment4 Test

    return order


@order.route("/", methods=['POST'])
def create():
    """
    Creates a new order from request data and adds it to the database.

    Returns:
        Response: A JSON response containing the created order's details 
        and a 201 status code.
    """
    # Extract order data from the request body
    data = request.get_json()

    # Create and initialize an Order object
    order = from_data_to_order(data)

    # Add the order to the database
    order.add()

    # Return the order details in the response
    return jsonify(order.to_dict()), 201


@order.route("/status", methods=['PUT'])
def put_status():
    """
    Updates the status of an existing order.

    Expects:
        JSON data containing:
        - "order_id": The unique ID of the order.
        - "order_status": The new status of the order.

    Returns:
        Response: A JSON response with the updated order details and a 
        200 status code, or an error message with a 400 or 404 status code.
    """
    # Extract data from the request body
    data = request.get_json()

    # Validate required fields
    if "order_id" not in data or "order_status" not in data:
        return jsonify({"error": "Missing data"}), 400

    # Initialize an Order object and check its existence
    order = Order(data["order_id"])
    order_exists = order.find()

    if not order_exists:
        # Return an error if the order does not exist
        return jsonify({"error": f"Order with id {data['order_id']} does not exist"}), 404

    # Update the order status and save changes
    order.order_status = OrderStatus(data["order_status"])
    order.update()

    # Return the updated order details
    return jsonify(order.to_dict()), 200


@order.route("/status/<id>", methods=['GET'])
def get_status(id):
    """
    Retrieves the status of an order by its ID.

    Args:
        id (str): The unique identifier of the order.

    Returns:
        Response: A JSON response containing the order's status and 
        a 200 status code, or an error message with a 404 status code 
        if the order does not exist.
    """
    # Initialize an Order object and check its existence
    order = Order(id)
    order_exists = order.find()

    if not order_exists:
        # Return an error if the order does not exist
        return jsonify({"error": f"Order with id {id} does not exist"}), 404

    # Return the order's status in the response
    return jsonify({"order_status": order.order_status.name}), 200
