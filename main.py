from flask import Flask
from api.user import user
from api.customer import customer
from api.vehicle import vehicle
from api.order import order

app = Flask(__name__)

app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(customer, url_prefix='/customer')
app.register_blueprint(vehicle, url_prefix='/vehicle')
app.register_blueprint(order, url_prefix='/order')

if __name__ == "__main__":
    app.run(debug=True)
