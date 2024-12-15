from helpers.ui import UI
from helpers.validate import Validate
from domain.location import Location, LocationList
from domain.vehicle import Vehicle
from domain.bike import Bike
from domain.truck import Truck
from domain.ship import Ship

class VehicleUI:
    """
    A class to handle user interface operations related to Vehicle objects.
    """

    def is_valid_id(self, vehicle: Vehicle, user_input) -> bool:
        """
        Check if the provided vehicle number is valid and not already in use.

        Args:
            vehicle (Vehicle): The vehicle object to check against.
            user_input (str): The vehicle number to validate.

        Returns:
            bool: True if the vehicle number is valid and not in use, False otherwise.
        """
        valid_vehicle_number = Validate.vehicle_number(user_input)
        response = vehicle.database.find_by_id(user_input)

        return valid_vehicle_number and response == None

    def set_id(self, vehicle: Vehicle) -> str:
        """
        Prompt the user for a valid vehicle number.

        Args:
            vehicle (Vehicle): The vehicle object to set the ID for.

        Returns:
            str: A valid vehicle number that isn't already in use.
        """
        while True:
            user_input = input("[i] Vehicle number (ABC123): ")
            
            if self.is_valid_id(vehicle, user_input):
                return user_input
            else:
                print("[i] Wrong vehicle number or vehicle already exists")

    def set_current_position(self) -> Location:
        """
        Prompt the user for a valid current position (city name).

        Returns:
            Location: A Location object representing the current position.
        """
        while True:
            user_input = input("[i] Current position (City name): ")
            
            current_position = LocationList().get_city_by_name(user_input)
            if current_position != None:
                return current_position
            else:
                print("[i] City name not found, please try again")

    def collect_data_for_new_vehicle(self, vehicle: Vehicle) -> None:
        """
        Collect and set data for a new vehicle.

        Args:
            vehicle (Vehicle): The vehicle object to collect data for.
        """
        vehicle.id = self.set_id(vehicle)
        vehicle.current_position = self.set_current_position()
        vehicle.add()

    def add_new_vehicle(self, user_name) -> None:
        """
        Guide the user through adding a new vehicle.

        Args:
            user_name (str): The name of the user adding the vehicle.
        """
        while True:
            UI.decorate_header("New Vehicle", 
                               user_name=user_name, 
                               with_footer_fill=True)
            user_input = input("Choose: (B)ike, (T)ruck or (S)hip: ")
            if Validate.user_entry(user_input, "bts"):
                break

        # Create the appropriate vehicle type based on user input
        match user_input.lower():
            case "b":
                vehicle = Bike()
            case "t":
                vehicle = Truck()
            case "s":
                vehicle = Ship()

        self.collect_data_for_new_vehicle(vehicle)