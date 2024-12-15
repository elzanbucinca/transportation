class Location:
    """Class to represent a geographical location with a city and a country."""
    
    def __init__(self,
                 city: str = None,
                 country: str = None
                ) -> None:
        self.city: str = city
        self.country: str = country


class LocationList:
    """Class to manage a list of locations with various cities."""
    
    def __init__(self) -> None:
        self.cities: list = self.add_cities()

    # Method to add predefined cities to the list of locations
    def add_cities(self) -> None:
        return [
            Location("Gothenburg", "Sweden"),
            Location("Lerum", "Sweden"),
            Location("Partille", "Sweden"),
            Location("Molndal", "Sweden"),
            Location("Stockholm", "Sweden"),
            Location("Malmo", "Sweden")
        ]
    
    # Method to get a location by the name of the city
    def get_city_by_name(self, city_name: str) -> Location:
        # Search for the location by city name (case insensitive)
        location = next((
            location for location in self.cities
            if location.city.lower() == city_name.lower()
        ), None)
        return location  # Return the found location or None if not found
