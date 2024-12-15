class Convert:
    """A utility class for type conversion methods."""
    
    @staticmethod
    def str_to_bool(value: str) -> bool:
        """
        Converts a string value to a boolean.

        Args:
            value (str): The string to be converted, expected to be 'true' or 'false'.

        Returns:
            bool: Returns True if the string is 'true' (case-insensitive), 
                  otherwise False.
        """
        if value is None:
            return False

        return value.lower() == 'true'
