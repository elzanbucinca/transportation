from enum import Enum
from database.database import Database


class PaymentMethod(Enum):
    """Enum to represent various payment methods."""
    NET_BANKING = 1
    CARD = 2
    DEBIT_CARD = 3


class PaymentDetails:
    DB_LOCATION = "database/payment.csv"  # File location for payment data

    def __init__(self,
                 transaction_id: str = None,
                 payment_method: PaymentMethod = None,
                 amount: float = None,
                 payment_status: str = None,
                 card_information: dict = None
                 ) -> None:
        self.transaction_id = transaction_id
        self.payment_method = payment_method
        self.amount = amount
        self.payment_status = payment_status
        self.card_information = card_information

        # Initialize the database connection
        self.get_database()

    def get_database(self) -> Database:
        """
        Initialize the database object with the payment details data.

        Returns:
            Database: The database object for storing/retrieving payment details data.
        """
        self.database = Database(self.DB_LOCATION, self.to_dict(), PaymentDetails.__name__)

    def to_dict(self) -> dict:
        """
        Convert the payment details to a dictionary for storage.

        Returns:
            dict: A dictionary containing all relevant payment details data.
        """
        return {
            'transaction_id': self.transaction_id,
            'payment_method': self.payment_method,
            'amount': self.amount,
            'payment_status': self.payment_status,
            'card_information': self.card_information
        }

    def from_dict_to_self(self, dictionary: dict) -> None:
        """
        Populate the payment's attributes from a dictionary.

        Args:
            dictionary (dict): A dictionary containing payment data.
        """
        if dictionary is not None:
            self.transaction_id = dictionary.get('transaction_id')
            self.payment_method = dictionary.get('payment_method')
            self.amount = dictionary.get('amount')
            self.payment_status = dictionary.get('payment_status')
            self.card_information = dictionary.get('card_information')

    def add(self) -> None:
        """
        Adds the current payment details instance to the database.
        """
        self.get_database()  # Ensure the database is set up
        self.database.add()  # Add the payment details data to the database

    def delete(self) -> None:
        """
        Deletes the current payment details instance from the database.
        """
        self.get_database()  # Ensure the database is set up
        self.database.delete()  # Delete the payment details data from the database

    def find(self) -> bool:
        """
        Find a payment detail in the database by its ID.

        Returns:
            bool: True if the payment detail is found, False otherwise.
        """
        self.get_database()  # Ensure the database is set up
        response = self.database.find_by_id(self.transaction_id)
        if response is not None:
            self.from_dict_to_self(response)  # Populate object with found data
            return True
        return False

    def update(self) -> None:
        """
        Update the payment details in the database with its current details.
        """
        self.get_database()  # Ensure the database is set up
        self.database.update()  # Update the payment details in the database
