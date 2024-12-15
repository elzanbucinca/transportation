from enum import Enum

# Enum to define the types of items
class ItemType(Enum):
    FRAGILE = 1
    SOLID = 2

# Class to represent the volume of an item with width, length, and height
class Volume:
    def __init__(self, 
                 width: float = None,
                 length: float = None,
                 height: float = None
                ) -> None:
        self.width = width
        self.length = length
        self.height = height

# Class to represent an item to be delivered
class Item:
    def __init__(self,
                    id: str = None,
                    price_per_kg: float = None,
                    volume: Volume = None,
                    weight: float = None,
                    type: ItemType = None
                 ) -> None:
        self.id = id
        self.price_per_kg = price_per_kg
        self.volume = volume
        self.weight = weight
        self.type = type

# Class to represent a collection of items
class ItemList:
    def __init__(self) -> None:
        self.items = self.add_items()  # Add items to the list upon initialization

    # Method to add predefined items to the item list
    def add_items(self) -> None:
        return [
            Item("0025", 10, Volume(1, 1, 1), 0.25, ItemType.SOLID),
            Item("0100", 10, Volume(1, 1, 1), 1.00, ItemType.SOLID),
            Item("0500", 50, Volume(1, 1, 1), 5.00, ItemType.FRAGILE),
            Item("2100", 50, Volume(1, 1, 1), 21.00, ItemType.FRAGILE),
            Item("7500", 50, Volume(1, 1, 1), 75.00, ItemType.FRAGILE),
        ]

    # Method to get an item by its unique ID
    def get_item_by_id(self, item_id: str) -> Item:
        # Search for the item in the list by its ID and return it if found
        item = next((item for item in self.items if item.id == item_id), None)
        return item  # Return the found item or None if not found
