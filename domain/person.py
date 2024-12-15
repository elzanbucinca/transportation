from database.database import Database
from helpers.convert import Convert
from domain.customer import Customer, CustomerType

# Person class inherits from Customer and represents a private person in the system
class Person(Customer):
    """
    Represents a person entity inheriting from Customer.

    Attributes:
        DB_LOCATION (str): Path to the database file for Person entities.
    """

    DB_LOCATION = "Transportation - v2/person.csv"

    def __init__(self, id: str = None,
                 full_name: str = None,
                 address: dict = None,
                 mobile_number: str = None,
                 email: str = None,
                 password: str = None,
                 is_user: bool = False) -> None:
        # Initialize parent class Customer with type set to PRIVATE
        super().__init__(
            id=id,
            type=CustomerType.PRIVATE
        )
        self.id: str = id
        self.full_name: str = full_name
        self.address: dict = address
        self.mobile_number: str = mobile_number
        self.email: str = email
        self.password: str = password
        self.is_user: bool = is_user

        # Initialize the database connection
        self.get_database()

    def get_database(self) -> Database:
        """
        Convert the person details to a dictionary for storage.

        Returns:
            dict: A dictionary containing all relevant person data.
        """
        self.database = Database(self.DB_LOCATION, self.to_dict(), Person.__name__)

    def to_dict(self) -> dict:
        """
        Converts the Person instance into a dictionary.
        
        Returns:
            dict: Dictionary representation of the Person instance.
        """
        return {
            'id': self.id,
            'full_name': self.full_name,
            'address': self.address,
            'mobile_number': self.mobile_number,
            'email': self.email,
            'password': self.password,
            'is_user': self.is_user
        }

    def from_dict_to_self(self, dictionary: dict) -> None:
        """
        Populates the Person instance with data from a dictionary.

        Args:
            dictionary (dict): Dictionary with Person data.
        """
        if dictionary is not None:
            # Map dictionary values to instance attributes
            self.id = dictionary.get('id')
            self.full_name = dictionary.get('full_name')
            self.address = dictionary.get('address')
            self.mobile_number = dictionary.get('mobile_number')
            self.email = dictionary.get('email')
            self.password = dictionary.get('password')
            # Convert 'is_user' to boolean
            self.is_user = Convert.str_to_bool(dictionary.get('is_user'))

    def add(self) -> None:
        """
        Adds the current person instance to the database.
        """
        self.get_database()  # Ensure the database is set up
        self.database.add()  # Add the company data to the database

    def delete(self) -> None:
        """
        Deletes the current person instance from the database.
        """
        self.get_database()  # Ensure the database is set up
        self.database.delete()  # Delete the company data from the database

    def find(self) -> bool:
        """
        Find a person in the database by its ID.

        Returns:
            bool: True if the person is found, False otherwise.
        """
        self.get_database()  # Ensure database is initialized
        response = self.database.find_by_id(self.id)  # Search by ID
        if response is not None:
            self.from_dict_to_self(response)  # Populate instance with data
            return True
        return False

    def update(self) -> None:
        """
        Update the person in the database with its current details.
        """
        self.get_database()  # Ensure database is initialized
        self.database.update()  # Update the record
