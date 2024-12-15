from domain.person import Person as User
from ui.order_ui import OrderUI
from ui.vehicle_ui import VehicleUI
from ui.customer_ui import CustomerUI
from ui.person_ui import PersonUI
from helpers.ui import UI
from helpers.validate import Validate

class MainUI:
    """
    Main user interface for managing application workflows such as user authentication,
    and navigating between orders, customers, and vehicles.

    Methods:
        get_user(): Handles user registration or sign-in.
        get_main_menu(): Displays the main menu for accessing orders, customers, or vehicles.
    """

    def __init__(self) -> None:
        """
        Initializes the MainUI class with a default user instance.
        """
        self.user = User()

    def get_user(self) -> None:
        """
        Handles user authentication. Allows the user to either register a new account
        or sign in to an existing one.
        """
        UI.decorate_header("(S)ign in (R)egister new user", with_footer_fill=True)

        while True:
            user_input = input("Please choose R to register, S to sign in: ")
            if Validate.user_entry(user_input, "rs"):  # Validate the user choice
                break

        match user_input.lower():
            case "r":  # Register a new user
                person = PersonUI().collect_data(is_user=True, is_updating=False)
                person.add()  # Add the new user to the database
                self.user = person  # Set the registered user as the current user
            case "s":  # Sign in an existing user
                UI.decorate_header("Sign in", with_footer_fill=True)
                person = PersonUI().authenticate()  # Authenticate the user
                self.user = person  # Set the authenticated user as the current user

    def get_main_menu(self) -> None:
        """
        Displays the main menu for the user, providing options to manage orders,
        customers, or vehicles.
        """
        user_name = self.user.full_name  # Display the current user's name
        UI.decorate_header(
            "(O)rders (C)ustomers (V)ehicles", user_name=user_name, with_footer_fill=True
        )

        while True:
            user_input = input(
                "Please choose O for orders, C for Customers, or V for vehicles: "
            )
            if Validate.user_entry(user_input, "ocv"):  # Validate menu choice
                break

        match user_input.lower():
            case "o":  # Navigate to the Orders menu
                order = OrderUI()
                order.get_order_menu(user_name)
            case "c":  # Navigate to the Customers menu
                customer = CustomerUI()
                customer.get_customer_menu(user_name)
            case "v":  # Navigate to the Vehicles menu
                vehicle = VehicleUI()
                vehicle.add_new_vehicle(user_name)
