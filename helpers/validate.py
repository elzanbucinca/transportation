import re

class Validate:
    """
    A utility class for validating various input formats using regular expressions.

    Methods:
        Various static methods to validate input strings against specific formats.
    """

    COMPANY_NUMBER_REGEX = r"^(\d{6}\-\d{4})$"
    EMAIL_REGEX = r"^[a-z0-9._%-]+@[a-z0-9.-]+\.[a-z]{2,}$"
    MOBILE_NUMBER_REGEX = r"^((((0{2}?)|(\+){1})46)|0)7[\d]{8}"
    PERSONAL_NUMBER_REGEX = (
        r"^((?:(?:[0-9]{2})(?:(?:0[13578]|1[02])(?:0[1-9]|[12][0-9]|3[01])|"
        r"(?:0[469]|11)(?:0[1-9]|[12][0-9]|30)|02(?:0[1-9]|1[0-9]|2[0-9])))(?:[0-9]{4}|-[0-9]{4}))$"
    )
    VEHICLE_NUMBER_REGEX = r"^([A-Z]{3}[0-9]{2}[A-Z0-9]{1})$"

    @staticmethod
    def company_number(input) -> bool:
        """
        Validates a company number format.

        Args:
            input (str): The input string to validate.

        Returns:
            bool: True if the input matches the company number format, otherwise False.
        """
        return Validate.regex(input, Validate.COMPANY_NUMBER_REGEX)

    @staticmethod
    def email(input) -> bool:
        """
        Validates an email address format.

        Args:
            input (str): The input string to validate.

        Returns:
            bool: True if the input matches the email format, otherwise False.
        """
        return Validate.regex(input, Validate.EMAIL_REGEX)

    @staticmethod
    def mobile(input) -> bool:
        """
        Validates a mobile number format.

        Args:
            input (str): The input string to validate.

        Returns:
            bool: True if the input matches the mobile number format, otherwise False.
        """
        return Validate.regex(input, Validate.MOBILE_NUMBER_REGEX)

    @staticmethod
    def number(input) -> bool:
        """
        Checks if the input can be converted to an integer.

        Args:
            input (str): The input string to validate.

        Returns:
            bool: True if the input is a valid integer, otherwise False.
        """
        try:
            int(input)  # Attempt to convert input to an integer
            return True
        except ValueError:  # Catch invalid integer conversion
            return False

    @staticmethod
    def person_full_name(input: str) -> bool:
        """
        Validates a person's full name.

        Args:
            input (str): The input string to validate.

        Returns:
            bool: True if the name contains only letters and single spaces, False otherwise.
        """
        space_count = input.count("  ")  # Check for multiple spaces
        is_not_alpha = any(
            not part_of_name.isalpha() for part_of_name in input.split(" ")
        )

        if is_not_alpha or space_count > 0:
            print(
                "[i] The name should contain only letters and "
                "no more than one whitespace in between."
            )
            return False
        else:
            return True

    @staticmethod
    def personal_number(input) -> bool:
        """
        Validates a personal identification number format.

        Args:
            input (str): The input string to validate.

        Returns:
            bool: True if the input matches the personal number format, otherwise False.
        """
        return Validate.regex(input, Validate.PERSONAL_NUMBER_REGEX)

    @staticmethod
    def regex(input, regex) -> bool:
        """
        Validates input against a given regular expression.

        Args:
            input (str): The input string to validate.
            regex (str): The regular expression pattern to match.

        Returns:
            bool: True if the input matches the regex, otherwise False.
        """
        result = re.fullmatch(regex, input)  # Perform regex matching
        return result is not None  # Return True if match found, otherwise False

    @staticmethod
    def user_entry(entry: str, expected_entry: str) -> bool:
        """
        Validates user input against expected entries.

        Args:
            entry (str): The user-provided input.
            expected_entry (str): The expected input string.

        Returns:
            bool: True if the input matches expected entries, otherwise False.
        """
        if entry.lower() in expected_entry:  # Compare lowercase versions for flexibility
            return True
        else:
            print("[i] Wrong input.")  # Notify the user of incorrect input
            return False

    @staticmethod
    def vehicle_number(input) -> bool:
        """
        Validates a vehicle registration number format.

        Args:
            input (str): The input string to validate.

        Returns:
            bool: True if the input matches the vehicle number format, otherwise False.
        """
        return Validate.regex(input, Validate.VEHICLE_NUMBER_REGEX)
