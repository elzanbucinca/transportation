from enum import Enum
from database.database import Database
from domain.customer import Customer
from domain.item import ItemList
from domain.location import Location
from domain.payment_details import PaymentDetails
from domain.person import Person
from domain.vehicle import Vehicle


class Priority(Enum):
    """
    Enum representing the priority levels of an order.
    """
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class OrderStatus(Enum):
    """
    Enum representing the status of an order.
    """
    PROCESSING = 1
    DELIVERED = 2
    CANCELLED = 3


class Order:
    """
    A class to represent an order, including all relevant details 
    and interactions with the database.
    """

    DB_LOCATION = "database/order.csv"

    def __init__(self,
                    id: str = None,
                    priority: Priority = Priority.LOW,
                    customer: Customer = None,
                    delivery_location: Location = None,
                    payment_details: PaymentDetails = None,
                    items: list = None,
                    total_weight: float = None,
                    order_status: OrderStatus = OrderStatus.PROCESSING,
                    order_date: str = None,
                    delivery_date: str = None,
                    vehicle: Vehicle = None) -> None:
        self.id = id
        self.priority = priority
        self.customer = customer
        self.delivery_location = delivery_location
        self.payment_details = payment_details
        self.items = items
        self.total_weight = total_weight
        self.order_status = order_status
        self.order_date = order_date
        self.delivery_date = delivery_date
        self.vehicle = vehicle

        # Initialize the database connection
        self.get_database()

    def get_database(self) -> Database:
        """
        Initialize the database object with the order data.

        Returns:
            Database: The database object for storing/retrieving order data.
        """
        self.database = Database(self.DB_LOCATION, self.to_dict(), Order.__name__)

    def to_dict(self) -> dict:
        """
        Convert the order details to a dictionary for storage.

        Returns:
            dict: A dictionary containing all relevant order data.
        """
        customer_id = None
        if self.customer is not None:
            customer_id = self.customer.id

        delivery_city = None
        delivery_country = None
        if self.delivery_location is not None:
            delivery_city = self.delivery_location.city
            delivery_country = self.delivery_location.country

        items = []
        if self.items is not None:
            for item in self.items:
                items.append(item.id)

        vehicle_id = None
        if self.vehicle is not None:
            vehicle_id = self.vehicle.id

        return {
            'id': self.id,
            'priority': self.priority.value,
            'customer_id': customer_id,
            'delivery_city': delivery_city,
            'delivery_country': delivery_country,
            'payment_details': self.payment_details,
            'items': items,
            'total_weight': self.total_weight,
            'order_status': self.order_status.value,
            'order_date': self.order_date,
            'delivery_date': self.delivery_date,
            'vehicle_id': vehicle_id,
        }

    def from_dict_to_self(self, dictionary: dict) -> None:
        """
        Populate the order's attributes from a dictionary.

        Args:
            dictionary (dict): A dictionary containing order data.
        """
        if dictionary is not None:
            # Set the customer by looking up the customer ID
            customer = Person(dictionary.get('customer_id'))
            if customer.find():
                self.customer = customer

            # Set the vehicle by looking up the vehicle ID
            vehicle = Vehicle(dictionary.get('vehicle_id'))
            if vehicle.find():
                self.vehicle = vehicle

            # Set the other order attributes from the dictionary
            self.id = dictionary.get('id')
            self.priority = Priority(int(dictionary.get('priority')))
            self.delivery_location = Location(
                dictionary.get('delivery_city'), dictionary.get('delivery_country')
            )
            self.payment_details = None
            self.items = self.from_list_record_to_items_list(dictionary.get('items'))
            self.total_weight = float(dictionary.get('total_weight'))
            self.order_status = OrderStatus(int(dictionary.get('order_status')))
            self.order_date = dictionary.get('order_date')
            self.delivery_date = dictionary.get('delivery_date')

    def from_list_record_to_items_list(self, items_ids_record: str) -> list:
        """
        Convert a list of item IDs to a list of item objects.

        Args:
            items_ids_record (str): A string representation of item IDs.

        Returns:
            list: A list of item objects.
        """
        items = []
        items_ids_string = items_ids_record.strip("[]").split(", ") if items_ids_record is not None else None
        items_ids = []
        if items_ids_string is not None:
            items_ids = [item_id.strip("'") for item_id in items_ids_string]
            for item_id in items_ids:
                items.append(ItemList().get_item_by_id(item_id))
        return items

    def add(self) -> None:
        """
        Adds the current order instance to the database.
        """
        self.get_database()  # Ensure the database is set up
        self.database.add()  # Add the order data to the database

    def delete(self) -> None:
        """
        Deletes the current company instance from the database.
        """
        self.get_database()  # Ensure the database is set up
        self.database.delete() # Delete the order data from the database

    def find(self) -> bool:
        """
        Find an order in the database by its ID.

        Returns:
            bool: True if the order is found, False otherwise.
        """
        self.get_database()  # Ensure the database is set up
        response = self.database.find_by_id(self.id)
        if response is not None:
            self.from_dict_to_self(response)  # Populate object with found data
            return True
        return False

    def update(self) -> None:
        """
        Update the order in the database with its current details.
        """
        self.get_database()  # Ensure the database is set up
        self.database.update()
