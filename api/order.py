from flask import Blueprint, request, jsonify
import uuid
from datetime import datetime
from domain.order import Order, OrderStatus
from domain.vehicle import Vehicle

order = Blueprint('order', __name__)


def from_data_to_order(data: dict):
    data["id"] = str(uuid.uuid4())[:4]
    data["total_weight"] = 0
    data["vehicle_id"] = ""
    data["order_status"] = OrderStatus.PROCESSING.value
    data["order_date"] = datetime.today().strftime("%Y%m%d")
    order = Order()
    order.from_dict_to_self(data)
    order.total_weight = round(sum([item.weight for item in order.items]), 2)

#     #### TESTS ####
#     # # Shipment1 Test
#     # order.vehicle = Vehicle().get_first_available(1, 5)
#     # # Shipment2 Test
#     # order.vehicle = Vehicle().get_first_available(12, 3)
#     # # Shipment3 Test
#     # order.vehicle = Vehicle().get_first_available(60, 4500)
#     # # Shipment4 Test
#     # order.vehicle = Vehicle().get_first_available(120, 2500)
    order.vehicle = Vehicle().get_first_available(len(order.items), order.total_weight)

    return order


@order.route("/", methods = ['POST'])
def create():
    data = request.get_json()
    order = from_data_to_order(data)
    order.add()
    return jsonify(order.to_dict()), 201


@order.route("/status", methods = ['PUT'])
def put_status():
    data = request.get_json()

    if "order_id" not in data or "order_status" not in data:
        return jsonify({"error": "Missing data"}), 400

    order = Order(data["order_id"])
    order_exists = order.find()

    if not order_exists:
        return jsonify({"error": f"Order with id {data["order_id"]} does not exist"}), 404
    
    order.order_status = OrderStatus(data["order_status"])
    order.update()
    return jsonify(order.to_dict()), 200


@order.route("/status/<id>", methods = ['GET'])
def get_status(id):
    order = Order(id)
    order_exists = order.find()

    if not order_exists:
        return jsonify({"error": f"Order with id {id} does not exist"}), 404

    return jsonify({"order_status": order.order_status.name}), 200

