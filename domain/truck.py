from domain.vehicle import Vehicle, VehicleType, VehicleStatusType
from domain.location import Location


class Truck(Vehicle):
    """
    Represents a Truck, inheriting from Vehicle.

    Attributes:
        MAX_ITEM_CAPACITY (int): Maximum item capacity of the truck.
        MAX_KG_CAPACITY (int): Maximum weight capacity in kg for the truck.
    """
    
    MAX_ITEM_CAPACITY = 100    # Maximum items the truck can carry
    MAX_KG_CAPACITY = 3000     # Maximum weight the truck can carry in kg

    def __init__(self,
                 id: str = None,
                 current_position: Location = None,
                 status: VehicleStatusType = VehicleStatusType.FREE,
                 remaining_item_capacity: int = MAX_ITEM_CAPACITY,
                 remaining_kg_capacity: int = MAX_KG_CAPACITY):
        """
        Initializes a Truck instance with specific capacities and status.

        Args:
            id (str): Unique identifier for the truck.
            current_position (Location): The truck's current position.
            status (VehicleStatusType): The current status of the truck.
            remaining_item_capacity (int): Remaining item capacity.
            remaining_kg_capacity (int): Remaining weight capacity in kg.
        """
        
        # Initialize parent class Vehicle with type set to TRUCK
        super().__init__(id=id,
                         current_position=current_position,
                         status=status,
                         remaining_item_capacity=remaining_item_capacity,
                         remaining_kg_capacity=remaining_kg_capacity,
                         type=VehicleType.TRUCK)
        
        # Initialize the database connection
        self.get_database()
