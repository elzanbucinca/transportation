import uuid
from datetime import datetime
from helpers.ui import UI
from helpers.validate import Validate
from domain.item import ItemList
from domain.location import Location, LocationList
from domain.order import Order, Priority, OrderStatus
from domain.person import Person
from domain.vehicle import Vehicle

class OrderUI:
    """
    A class to manage the user interface for creating, retrieving, 
    and updating orders.
    """

    def set_id(self) -> str:
        """
        Generate a unique 4-character identifier for an order.
        Returns:
            str: A unique 4-character ID.
        """
        full_id = uuid.uuid4()
        return str(full_id)[:4]
    

    def get_order_menu(self, user_name) -> None:
        """
        Display the main order menu and handle user choices for creating, 
        retrieving, or updating orders.

        Args:
            user_name (str): The name of the current user.
        """
        UI.decorate_header("(N)ew order - (R)etrieve order status - (U)pdate order status",
                           user_name=user_name, with_footer_fill=True)

        # Prompt the user for a valid menu option.
        while True:
            user_input = input("Please choose N to add new order, R to retrieve "
                               "an order's status or U to update an order's status: ")
            if Validate.user_entry(user_input, "nru"):
                break

        # Handle the user's choice.
        match user_input.lower():
            case "n":
                self.add_new_order(user_name)
            case "r":
                self.retrieve_order_status(user_name)
            case "u":
                self.update_order_status(user_name)

    def get_order(self) -> Order:
        """
        Prompt the user to provide an order ID and return the corresponding order.

        Returns:
            Order: The order object if found.
        """
        while True:
            user_input = input("[i] Id of order: ")
            order = Order(user_input)
            order_exists = order.find()
            if order_exists:
                return order
            else:
                print("[i] Order not found, please try again")

    def set_priority(self) -> Priority:
        """
        Prompt the user to set the priority for an order.

        Returns:
            Priority: The priority level of the order.
        """
        while True:
            user_input = input("[i] Order priority - (L)ow, (M)edium or (H)igh: ")
            
            if Validate.user_entry(user_input, "lmh"):
                # Map the user input to the corresponding priority enum.
                match user_input.lower():
                    case "l":
                        return Priority.LOW
                    case "m":
                        return Priority.MEDIUM
                    case "h":
                        return Priority.HIGH
            else:
                print("[i] Wrong input, please try again")

    def set_customer(self):
        """
        Prompt the user to provide a customer ID and validate its existence.

        Returns:
            Person: The customer object.
        """
        while True:
            user_input = input("[i] Id of Customer: ")
            person = Person(user_input)
            person_exists = person.find()
            if person_exists:
                return person
            else:
                print("[i] User not found, please try again")

    def set_delivery_location(self) -> Location:
        """
        Prompt the user to input a delivery location and validate it.

        Returns:
            Location: The delivery location object.
        """
        while True:
            user_input = input("[i] Delivery location (City name): ")
            delivery_location = LocationList().get_city_by_name(user_input)
            if delivery_location is not None:
                return delivery_location
            else:
                print("[i] City name not found, please try again")

    def set_items(self) -> list:
        """
        Collect and validate items for the order.

        Returns:
            list: A list of item objects included in the order.
        """
        print("==== Order Items ====")
        items = []
        while True:
            user_input = input("[i] Add item by id or (D)one: ")
            if user_input.lower() == "d":
                break

            # Validate and add the item.
            item = ItemList().get_item_by_id(user_input)
            if item is not None:
                items.append(item)
                print(f"[i] Item {item.id} added")
            else:
                print("[i] Item not found, please try again")
        
        print("=====================")
        return items

    def set_order_status(self) -> Priority:
        """
        Prompt the user to set the order status.

        Returns:
            Priority: The new order status.
        """
        while True:
            user_input = input("[i] Order status - (P)rocessing, (D)elivered or (C)ancelled: ")
            
            if Validate.user_entry(user_input, "pdc"):
                # Map user input to the order status.
                match user_input.lower():
                    case "p":
                        return OrderStatus.PROCESSING
                    case "d":
                        return OrderStatus.DELIVERED
                    case "c":
                        return OrderStatus.CANCELLED
            else:
                print("[i] Wrong input, please try again")

    def set_vehicle(self, number_of_items, weight) -> str:
        """
        Find and return the first available vehicle that can handle the given 
        order's items and weight.

        Args:
            number_of_items (int): The number of items in the order.
            weight (float): The total weight of the items.

        Returns:
            str: The ID of the allocated vehicle.
        """
        return Vehicle().get_first_available(number_of_items, weight)

    def is_valid_delivery_date(self, delivery_date):
        """
        Validate if the given delivery date is in the correct format and in the future.

        Args:
            delivery_date (str): The delivery date in yyyymmdd format.

        Returns:
            bool: True if the date is valid, False otherwise.
        """
        if len(delivery_date) != 8:
            print("Invalid format: Input must be exactly 8 characters long.")
            return False

        if not delivery_date.isdigit():
            print("Invalid format: Input must only contain digits.")
            return False

        # Validate the date using datetime.
        year = int(delivery_date[:4])
        month = int(delivery_date[4:6])
        day = int(delivery_date[6:])
        try:
            delivery_date = datetime(year, month, day)
            if delivery_date < datetime.today():
                print("Invalid date: Delivery date must be in the future.")
                return False
            return True
        except ValueError:
            print("Invalid date: Check if the month and date are correct.")
            return False

    def set_delivery_date(self) -> str:
        """
        Prompt the user to input a valid delivery date.

        Returns:
            str: The validated delivery date in yyyymmdd format.
        """
        while True:
            user_input = input("[i] Delivery date (yyyymmdd): ")
            if self.is_valid_delivery_date(user_input):
                return user_input

    def collect_data(self, order: Order) -> None:
        """
        Collect and set all required data for creating a new order.

        Args:
            order (Order): The order object to populate.
        """
        order.id = self.set_id()
        order.priority = self.set_priority()
        order.customer = self.set_customer()
        order.delivery_location = self.set_delivery_location()
        order.items = self.set_items()
        order.total_weight = round(sum([item.weight for item in order.items]), 2)
        order.vehicle = self.set_vehicle(len(order.items), order.total_weight)
        order.delivery_date = self.set_delivery_date()
        order.order_date = datetime.today().strftime("%Y%m%d")
        order.add()

    def add_new_order(self, user_name) -> None:
        """
        Create a new order and allocate necessary resources.

        Args:
            user_name (str): The name of the user creating the order.
        """
        UI.decorate_header("New Order", user_name=user_name, with_footer_fill=True)
        order = Order()
        self.collect_data(order)

        if order.vehicle is not None:
            # Update vehicle capacities after assignment.
            order.vehicle.remaining_item_capacity -= len(order.items)
            order.vehicle.remaining_kg_capacity -= order.total_weight
            order.vehicle.update()

        print(f"[i] Order with id:{order.id} added successfully")

    def retrieve_order_status(self, user_name) -> None:
        """
        Retrieve and display the status of an existing order.

        Args:
            user_name (str): The name of the user requesting the order status.
        """
        UI.decorate_header("Retrieve Order Status", user_name=user_name, with_footer_fill=True)
        order = self.get_order()

        # Display order details.
        print("==== Order Status ====")
        print(f"Order ID: {order.id}")
        print(f"Order Status: {OrderStatus(order.order_status).name.title()}")
        print(f"Order Date: {order.order_date}")
        print(f"Delivery Date: {order.delivery_date}")

    def update_order_status(self, user_name) -> None:
        """
        Update the status of an existing order.

        Args:
            user_name (str): The name of the user updating the order.
        """
        UI.decorate_header("Retrieve Order Status", user_name=user_name, with_footer_fill=True)
        order = self.get_order()
        order.order_status = self.set_order_status()
        order.update()
        # Restore vehicle capacities if the order is completed or cancelled
