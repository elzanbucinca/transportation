from enum import Enum
from database.database import Database
from domain.location import Location

# Enum for vehicle types
class VehicleType(Enum):
    BIKE = 1
    TRUCK = 2
    SHIP = 3

# Enum for vehicle status types
class VehicleStatusType(Enum):
    FREE = 1
    LOADING = 2
    BUSY = 3
    NOT_WORKING = 4

# Vehicle class representing different vehicle types and their status
class Vehicle:
    DB_LOCATION = "Transportation - v2/vehicle.csv" 

    def __init__(self, 
                    id: str = None,
                    current_position: Location = None,
                    status: VehicleStatusType = None,
                    remaining_item_capacity: int = None,
                    remaining_kg_capacity: int = None,
                    type: VehicleType = None
                 ):
        self.id = id
        self.current_position = current_position
        self.status = status
        self.remaining_item_capacity = remaining_item_capacity
        self.remaining_kg_capacity = remaining_kg_capacity
        self.type = type

    def to_dict(self) -> dict:
        """
        Convert the vehicle details to a dictionary for storage.

        Returns:
            dict: A dictionary containing all relevant vehicle data.
        """
        current_position_city = None
        current_position_country = None
        # Check if current position is set
        if self.current_position != None:
            current_position_city = self.current_position.city
            current_position_country = self.current_position.country

        # Convert status to its numeric value
        status = None
        if self.status != None:
            status = self.status.value

        # Convert vehicle type to its numeric value
        type = None
        if self.type != None:
            type = self.type.value

        # Return vehicle attributes as a dictionary
        return {
            'id': self.id,
            'current_position_city': current_position_city,
            'current_position_country': current_position_country,
            'status': status,
            'remaining_item_capacity': self.remaining_item_capacity,
            'remaining_kg_capacity': self.remaining_kg_capacity,
            'type': type,
        }
    
    def get_database(self) -> Database:
        """
        Initialize the database object with the vehicle data.

        Returns:
            Database: The database object for storing/retrieving vehicle data.
        """
        self.database = Database(self.DB_LOCATION, self.to_dict(), Vehicle.__name__)

    def from_list_to_self(self, vehicle: list) -> None:
        """
        Populate the vehicles's attributes from a list.

        Args:
            vehicle (list): A list containing vehicle data.
        """
        if vehicle != None:
            # Get the dictionary headers for mapping list values
            headers = list(self.to_dict())
            id_index = headers.index("id")
            city_index = headers.index("current_position_city")
            country_index = headers.index("current_position_country")
            status_index = headers.index("status")
            ramaining_item_capacity_index = headers.index("remaining_item_capacity")
            remaining_kg_capacity_index = headers.index("remaining_kg_capacity")
            type_index = headers.index("type")

            # Assign values to the vehicle object based on the list
            self.id = vehicle[id_index]
            self.current_position = Location(vehicle[city_index], vehicle[country_index])
            self.status = VehicleStatusType(int(vehicle[status_index]))
            self.remaining_item_capacity = int(vehicle[ramaining_item_capacity_index])
            self.remaining_kg_capacity = float(vehicle[remaining_kg_capacity_index])
            self.type = VehicleType(int(vehicle[type_index]))

    def from_dict_to_self(self, dictionary: dict) -> None:
        """
        Populate the vehicle's attributes from a dictionary.

        Args:
            dictionary (dict): A dictionary containing vehicle data.
        """
        if dictionary != None:
            # Assign values to the vehicle object based on the dictionary
            self.id = dictionary.get('id')
            city = dictionary.get('current_position_city')
            country = dictionary.get('current_position_country')
            self.current_position = Location(city, country)
            self.status = VehicleStatusType(int(dictionary.get('status')))
            self.remaining_item_capacity = int(dictionary.get('remaining_item_capacity'))
            self.remaining_kg_capacity = float(dictionary.get('remaining_kg_capacity'))
            self.type = VehicleType(int(dictionary.get('type')))

    def add(self) -> None:
        """
        Adds the current vehicle instance to the database.
        """
        self.get_database()  # Ensure the database is set up
        self.database.add()  # Add vehicle data to the database

    def find(self) -> bool:
        """
        Find a vehicle in the database by its ID.

        Returns:
            bool: True if the vehicle is found, False otherwise.
        """
        self.get_database()  # Ensure the database is set up
        response = self.database.find_by_id(self.id)
        if response != None:
            self.from_dict_to_self(response)  # Populate object with found data
            return True
        return False

    def get_first_available(self, number_of_items: int, weight: int):
        """
        Gets the first available vehicle with sufficient capacity.
        
        Returns:
            Vehicle: The first available vehicle with sufficient capacity
            None: if no vehicle is available.
        """
        self.get_database()  # Ensure the database is set up
        # Find all vehicles that are free
        available_vehicles = self.database.find_by_field_name("status", 
                                VehicleStatusType.FREE.value)

        # Get headers for capacity checks
        headers = list(self.to_dict())
        ramaining_item_capacity_index = headers.index("remaining_item_capacity")
        remaining_kg_capacity_index = headers.index("remaining_kg_capacity")

        # Sort available vehicles by item capacity
        available_vehicles = sorted(available_vehicles, 
                                key=lambda x: int(x[ramaining_item_capacity_index]))

        # Check if any vehicle meets the requirements
        for vehicle in available_vehicles:
            if int(vehicle[ramaining_item_capacity_index]) >= number_of_items \
                and float(vehicle[remaining_kg_capacity_index]) >= weight:
                    self.from_list_to_self(vehicle)  # Populate vehicle data
                    return self  # Return the available vehicle

        return None  # No available vehicle found

    def update(self) -> None:
        """
        Update the vehicle in the database with its current details.
        """
        self.get_database()  # Ensure the database is set up
        self.database.update()  # Update the vehicle in the database
