from helpers.ui import UI
from helpers.validate import Validate
from helpers.address import Address
from helpers.reference_person import ReferencePerson
from domain.company import Company
from domain.person import Person

class CompanyUI:
    """
    Handles user interactions related to company creation and management.
    
    Methods:
        is_valid_id(user_input): Validates company ID format and uniqueness.
        is_valid_company_name(name): Validates the format of a company name.
        set_id(): Prompts the user to input and validate a company ID.
        set_company_name(): Prompts the user to input and validate a company name.
        set_invoice_email(): Prompts the user to input and validate an invoice email.
        set_related_users(): Collects and validates related user IDs for a company.
        collect_data(is_updating): Collects company details for creation or updating.
    """

    def is_valid_id(self, user_input) -> bool:
        """
        Validates the company ID format and ensures it doesn't already exist.

        Args:
            user_input (str): The input company ID.

        Returns:
            bool: True if the ID is valid and doesn't exist, otherwise False.
        """
        valid_company_number = Validate.company_number(user_input)
        company_exists = Company(user_input).find()

        return valid_company_number and not company_exists

    def is_valid_company_name(self, name: str) -> bool:
        """
        Validates the company name format.

        Args:
            name (str): The input company name.

        Returns:
            bool: True if the name is valid, otherwise False.
        """
        space_count = name.count("  ")  # Check for multiple consecutive spaces

        if space_count > 0:
            print("[i] The name should contain no more than one whitespace in between.")
            return False
        else:
            return True

    def set_id(self) -> str:
        """
        Prompts the user to input and validate a company ID.

        Returns:
            str: A valid company ID.
        """
        while True:
            user_input = input("[i] Company number: ")

            if self.is_valid_id(user_input):
                return user_input
            else:
                print("[i] Wrong company number or company already exists.")

    def set_company_name(self) -> str:
        """
        Prompts the user to input and validate a company name.

        Returns:
            str: A valid company name.
        """
        while True:
            user_input = input("[i] Company name: ")

            if self.is_valid_company_name(user_input):
                return user_input

    def set_invoice_email(self) -> str:
        """
        Prompts the user to input and validate an invoice email.

        Returns:
            str: A valid invoice email address.
        """
        while True:
            user_input = input("[i] Invoice email: ")

            if Validate.email(user_input):
                return user_input

    def set_related_users(self) -> list:
        """
        Collects and validates related user IDs for a company.

        Returns:
            list: A list of valid related user IDs.
        """
        while True:
            user_total = input("[i] How many users do you want to add to this company: ")
            
            if Validate.number(user_total):  # Ensure input is a number
                break

        users_list = []  # List to store valid user IDs
        user_count = 1
        while user_count <= int(user_total):  # Loop until all users are added
            user_input = input(f"[i] Id of Person {user_count}: ")
            # Check if user exists and is a valid user
            person = Person(user_input).database.find_by_id(user_input)
            if person is not None and person['is_user'] == 'True':
                users_list.append(user_input)
                user_count += 1
            else:
                print("[i] User not found, please try again.")

        return users_list

    def collect_data(self, is_updating: bool) -> Company:
        """
        Collects company details for creation or updating.

        Args:
            is_updating (bool): Whether the operation is an update.

        Returns:
            Company: A Company object populated with the collected data.
        """
        company = Company() 

        if not is_updating:  # Set ID only for new companies
            company.id = self.set_id()

        # Collect other company details
        company.company_name = self.set_company_name()
        company.company_address = Address().set_addresss()
        company.reference_person = ReferencePerson().set_reference_person()
        company.invoice_email = self.set_invoice_email()
        company.related_users = self.set_related_users()

        return company
