from helpers.ui import UI
from helpers.validate import Validate
from helpers.address import Address
from domain.person import Person

class PersonUI:
    """
    A class to handle user interface operations related to Person objects.
    """

    def is_valid_id(self, user_input) -> bool:
        """
        Check if the provided personal number is valid and not already in use.

        Args:
            user_input (str): The personal number to validate.

        Returns:
            bool: True if the personal number is valid and not in use, False otherwise.
        """
        valid_personal_number = Validate.personal_number(user_input)
        person_exists = Person(user_input).find()

        return valid_personal_number and not person_exists
    
    def set_id(self) -> None:
        """
        Prompt the user for a valid personal number.

        Returns:
            str: A valid personal number that doesn't belong to an existing person.
        """
        while True:
            user_input = input("[i] Personal number YYMMDD-NNNN: ")
            
            if self.is_valid_id(user_input):
                return user_input
            else:
                print("[i] Wrong personal number or person already exists")

    def set_full_name(self):
        """
        Prompt the user for a valid full name.

        Returns:
            str: A valid full name.
        """
        while True:
            user_input = input("[i] Full name: ")

            if Validate.person_full_name(user_input):
                return user_input
    
    def set_password(self):
        """
        Prompt the user for a password.

        Returns:
            str: The entered password.
        """
        user_input = input("[i] Password: ")     
        return user_input
    
    def set_mobile_number(self):
        """
        Prompt the user for a valid mobile number.

        Returns:
            str: A valid mobile number without spaces or dashes.
        """
        while True:
            user_input = input("[i] Mobile number (no spaces or dashes): ")

            if Validate.mobile(user_input):
                return user_input

    def set_email(self):
        """
        Prompt the user for a valid email address.

        Returns:
            str: A valid email address.
        """
        while True:
            user_input = input("[i] Email address: ")

            if Validate.email(user_input):
                return user_input

    def collect_data(self, is_user, is_updating) -> Person:
        """
        Collect all necessary data to create or update a Person object.

        Args:
            is_user (bool): Whether the person is a user of the system.
            is_updating (bool): Whether we're updating an existing person.

        Returns:
            Person: A Person object with collected data.
        """
        person = Person()

        if (not is_updating):
            person.id = self.set_id()

        if (is_user):
            person.password = self.set_password()
            person.is_user = True

        person.full_name = self.set_full_name()
        person.address = Address().set_addresss()
        person.mobile_number = self.set_mobile_number()
        person.email = self.set_email()
        
        return person
    
    def authenticate(self) -> None:
        """
        Authenticate a user by prompting for personal number and password.

        Returns:
            Person: An authenticated Person object if successful, None otherwise.
        """
        while True:
            user_id = input("[i] Your personal number YYMMDD-NNNN: ")
            user_password = input("[i] Your password: ")

            person = Person(user_id)
            person_exists = person.find()

            if person_exists \
                and user_password == person.password \
                and person.is_user:
                    return person
            else:
                print("[i] Wrong user name or password, please try again")