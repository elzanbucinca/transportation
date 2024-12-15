from domain.vehicle import Vehicle, VehicleType, VehicleStatusType
from domain.location import Location


class Bike(Vehicle):
    """
    Represents a Bike, inheriting from Vehicle.

    Attributes:
        MAX_ITEM_CAPACITY (int): Maximum item capacity of the bike.
        MAX_KG_CAPACITY (int): Maximum weight capacity in kg for the bike.
    """
    
    MAX_ITEM_CAPACITY = 2  # Maximum items the bike can carry
    MAX_KG_CAPACITY = 10   # Maximum weight the bike can carry in kg

    def __init__(self,
                 id: str = None,
                 current_position: Location = None,
                 status: VehicleStatusType = VehicleStatusType.FREE,
                 remaining_item_capacity: int = MAX_ITEM_CAPACITY,
                 remaining_kg_capacity: int = MAX_KG_CAPACITY):
        """
        Initializes a Bike instance with specific capacities and status.
        
        Args:
            id (str): Unique identifier for the bike.
            current_position (Location): The bike's current position.
            status (VehicleStatusType): The current status of the bike.
            remaining_item_capacity (int): Remaining item capacity.
            remaining_kg_capacity (int): Remaining weight capacity in kg.
        """
        
        # Initialize parent class Vehicle with type set to BIKE
        super().__init__(id=id,
                         current_position=current_position,
                         status=status,
                         remaining_item_capacity=remaining_item_capacity,
                         remaining_kg_capacity=remaining_kg_capacity,
                         type=VehicleType.BIKE)
        
        # Initialize the database connection
        self.get_database()
