from domain.vehicle import Vehicle, VehicleType, VehicleStatusType
from domain.location import Location


class Ship(Vehicle):
    """
    Represents a Ship, inheriting from Vehicle.

    Attributes:
        MAX_ITEM_CAPACITY (int): Maximum item capacity of the ship.
        MAX_KG_CAPACITY (int): Maximum weight capacity in kg for the ship.
    """
    
    MAX_ITEM_CAPACITY = 1000   # Maximum items the ship can carry
    MAX_KG_CAPACITY = 100000   # Maximum weight the ship can carry in kg

    def __init__(self,
                 id: str = None,
                 current_position: Location = None,
                 status: VehicleStatusType = VehicleStatusType.FREE,
                 remaining_item_capacity: int = MAX_ITEM_CAPACITY,
                 remaining_kg_capacity: int = MAX_KG_CAPACITY):
        """
        Initializes a Ship instance with specific capacities and status.

        Args:
            id (str): Unique identifier for the ship.
            current_position (Location): The ship's current position.
            status (VehicleStatusType): The current status of the ship.
            remaining_item_capacity (int): Remaining item capacity.
            remaining_kg_capacity (int): Remaining weight capacity in kg.
        """
        
        # Initialize parent class Vehicle with type set to SHIP
        super().__init__(id=id,
                         current_position=current_position,
                         status=status,
                         remaining_item_capacity=remaining_item_capacity,
                         remaining_kg_capacity=remaining_kg_capacity,
                         type=VehicleType.SHIP)
        
        # Initialize the database connection
        self.get_database()
