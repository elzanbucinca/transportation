from enum import Enum

# Enum to define the types of customers
class CustomerType(Enum):
    COMPANY = 1  # Company customer type
    PRIVATE = 2  # Private individual customer type

# Customer class represents a general customer with an ID and type
class Customer:
    def __init__(self, id: str = None,  # Customer ID
                       type: CustomerType = None):  # Type (COMPANY or PRIVATE)
        self.id = id,  # Initialize customer ID (stored as a tuple)
        self.type = type  # Initialize customer type (COMPANY or PRIVATE)
