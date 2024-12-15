from database.database import Database
from domain.customer import Customer, CustomerType

# Company class inherits from Customer and represents a company/corporate in the system
class Company(Customer):
    DB_LOCATION = "Transportation - v2/company.csv"

    def __init__(self, id: str = None,
                       company_name: str = None,
                       company_address: dict = None,
                       reference_person: dict = None,
                       invoice_email: str = None,
                       related_users: list = None) -> None:
        # Initialize parent class Customer with type set to COMPANY
        super().__init__(id=id, type=CustomerType.COMPANY)
        self.id: str = id
        self.company_name: str = company_name
        self.company_address: dict = company_address
        self.reference_person: dict = reference_person
        self.invoice_email: str = invoice_email
        self.related_users: list = related_users

        # Initialize the database connection
        self.get_database()

    def get_database(self) -> Database:
        """
        Initialize the database object with the company data.

        Returns:
            Database: The database object for storing/retrieving company data.
        """
        self.database = Database(self.DB_LOCATION, self.to_dict(), Company.__name__)

    def to_dict(self) -> dict:
        """
        Convert the company details to a dictionary for storage.

        Returns:
            dict: A dictionary containing all relevant company data.
        """
        return {
            'id': self.id,
            'company_name': self.company_name,
            'company_address': self.company_address,
            'reference_person': self.reference_person,
            'invoice_email': self.invoice_email,
            'related_users': self.related_users
        }

    def from_dict_to_self(self, dictionary: dict) -> None:
        """
        Populate the company's attributes from a dictionary.

        Args:
            dictionary (dict): A dictionary containing company data.
        """
        if dictionary != None:
            self.id = dictionary.get('id')
            self.company_name = dictionary.get('company_name')
            self.company_address = dictionary.get('company_address')
            self.reference_person = dictionary.get('reference_person')
            self.invoice_email = dictionary.get('invoice_email')
            self.related_users = dictionary.get('related_users')

    def add(self) -> None:
        """
        Adds the current company instance to the database.
        """
        self.get_database()  # Ensure the database is set up
        self.database.add()  # Add the company data to the database

    def delete(self) -> None:
        """
        Deletes the current company instance from the database.
        """
        self.get_database()  # Ensure the database is set up
        self.database.delete()  # Delete the company data from the database

    def find(self) -> bool:
        """
        Find a company in the database by its ID.

        Returns:
            bool: True if the company is found, False otherwise.
        """
        self.get_database()  # Ensure the database is set up
        response = self.database.find_by_id(self.id)
        if response != None:
            self.from_dict_to_self(response)  # Populate object with found data
            return True
        return False

    def update(self) -> None:
        """
        Update the company in the database with its current details.
        """
        self.get_database()  # Ensure the database is set up
        self.database.update()  # Update the company in the database
