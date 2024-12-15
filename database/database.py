import csv
import os.path

class Database:
    """
    A class to represent and manage a CSV-based database.

    Attributes:
        path (str): The path to the CSV file.
        dictionary (dict): Data structure to hold record data.
        object_name (str): Name of the object being managed in the database.
    """

    def __init__(self, path: str = None, dictionary: dict = None, 
                 object_name: str = None):
        """
        Initializes Database with file path, record dictionary, and object name.
        
        If the file does not exist, it creates a new database.
        """
        self.path = path
        self.dictionary = dictionary
        self.object_name = object_name

        # Check if the file exists; if not, create a new database
        file_exists = os.path.exists(self.path)
        if not file_exists:
            self.create_database()

    def add(self):
        """
        Adds a new record to the database if it doesn't already exist.
        
        Raises:
            ValueError: If the record ID already exists in the database.
        """
        try:
            # Extract values from dictionary to get record ID
            record_values = list(self.dictionary.values())
            record_id = record_values[0]
            if self.is_valid_database():
                # Check if a record with the same ID already exists
                existing_record = self.find_by_id(record_values[0])

                if existing_record:
                    raise ValueError(
                        f"[i] {self.object_name} with id {record_id} already exists"
                    )

                # Append new record to the CSV file
                with open(self.path, mode='a', newline='') as my_csv:
                    fieldnames = self.dictionary.keys()
                    csv_writer = csv.DictWriter(my_csv, delimiter=',', 
                                                fieldnames=fieldnames)
                    csv_writer.writerow(self.dictionary)
        except Exception as error:
            print(f"[i] Failed to add {self.object_name.lower()} with id: "
                  f"{record_id}. \n{error}")

    def create_database(self):
        """
        Creates a new CSV database with headers from the dictionary keys.
        
        Returns:
            bool: True if the database is created successfully.
        """
        if self.is_valid_path_and_dictionary():
            # Create a new CSV file with headers from dictionary keys
            with open(self.path, mode='w', newline='') as csv_file:
                field_names = list(self.dictionary.keys())
                csv_writer = csv.DictWriter(csv_file, fieldnames=field_names, 
                                            delimiter=',')
                csv_writer.writeheader()
                return True

    def delete(self) -> bool:
        """
        Deletes a record from the database by record ID.

        Returns:
            bool: True if deletion is successful, False otherwise.
        """
        try:
            # Retrieve record ID for deletion
            record_values = list(self.dictionary.values())
            record_id = record_values[0]
            if self.is_valid_database():
                content = list()  # Store all records except the deleted one
                record_found = False

                # Read records and identify target for deletion
                with open(self.path, mode='r') as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    for row in csv_reader:
                        if row[0] == record_id:
                            record_found = True
                        else:
                            content.append(row)

                # Save updated content without the deleted record
                if record_found:
                    self.save_content(content)
                    print(f"[i] Successfully deleted {self.object_name.lower()} "
                          f"with id {record_id}")
                else:
                    print(f"[i] {self.object_name} with id {record_id} not found")
        except Exception as error:
            print(f"[i] Failed to delete {self.object_name.lower()} with id: "
                  f"{record_id}. \n{error}")

    def find_by_id(self, id: str) -> dict:
        """
        Finds a record by its ID.

        Args:
            id (str): The ID to search for.

        Returns:
            dict: The record data if found, None otherwise.
        """
        if self.is_valid_database():
            # Open file and skip header row to find matching ID
            with open(self.path, 'r') as my_file:
                csv_reader = csv.reader(my_file, delimiter=',')
                next(csv_reader)  # Skip the header row

                result = [row for row in csv_reader if id == row[0]]

                if len(result) != 0:
                    # Map found row data to dictionary keys
                    response = self.dictionary.copy()
                    headers = list(self.dictionary.keys())

                    for i, value in enumerate(result[0]):
                        response[headers[i]] = value

                    return response

        return None

    def find_by_field_name(self, field: str, value: str) -> list:
        """
        Finds records by a specified field and value.

        Args:
            field (str): The field name to search within.
            value (str): The value to match.

        Returns:
            list: Records that match the field and value.
        """
        if self.is_valid_database():
            headers = list(self.dictionary.keys())
            if field not in headers:
                raise ValueError(
                    f"[i] Field '{field}' not found in the database headers"
                )
            # Locate the field's index to compare values
            field_index = headers.index(field)

            with open(self.path, 'r') as my_file:
                csv_reader = csv.reader(my_file, delimiter=',')
                next(csv_reader)  # Skip the header row
                result = [row for row in csv_reader if 
                          str(value).strip().lower() == 
                          row[field_index].strip().lower()]

                return result

        return None

    def update(self) -> bool:
        """
        Updates an existing record with new values.

        Returns:
            bool: True if the update is successful, False otherwise.
        """
        record_new_values = list(self.dictionary.values())
        record_id = record_new_values[0]
        try:
            if self.is_valid_database():
                content = list()
                record_found = False

                # Identify and replace record with new values
                with open(self.path, mode='r') as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    for existing_record_values in csv_reader:
                        if existing_record_values[0] == record_new_values[0]:
                            record_found = True
                            content.append(record_new_values)
                        else:
                            content.append(existing_record_values)

                # Save updated records back to file
                if record_found:
                    self.save_content(content)
                    print(f"[i] {self.object_name} with id: {record_id} "
                          "successfully updated")
                else:
                    print(f"[i] {self.object_name} with id {record_id} not found")
        except:
            print(f"[i] Failed to update {self.object_name.lower()} with id: "
                  f"{record_id}")

    def get_existing_field_names(self) -> list:
        """
        Retrieves the header field names from the CSV file.

        Returns:
            list: List of header field names.
        
        Raises:
            ValueError: If no header is found in the file.
        """
        header = list()
        with open(self.path, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            header = next(csv_reader, None)  # get first row as header

        if len(header) == 0:
            raise ValueError(f"[i] No header found!")

        return header

    def save_content(self, content: list) -> bool:
        """
        Saves updated content to the CSV file.

        Args:
            content (list): The data to write back to the CSV.

        Returns:
            bool: True if save is successful.
        """
        # Write updated content to the CSV file
        with open(self.path, mode='w', newline="") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerows(content)

        return True

    def is_valid_path_and_dictionary(self) -> bool:
        """
        Checks if path is a CSV file and dictionary is valid.

        Returns:
            bool: True if path and dictionary are valid.
        
        Raises:
            ValueError: If the path or dictionary is invalid.
        """
        # Verify the path ends with .csv and dictionary is a valid dict
        path_ok = isinstance(self.path, str) and self.path.endswith('csv')
        dictionary_ok = isinstance(self.dictionary, dict)

        if path_ok and dictionary_ok:
            return True
        else:
            raise ValueError(f"[i] Wrong path: {self.path} or wrong dictionary = "
                             f"{self.dictionary}")

    def is_valid_database(self) -> bool:
        """
        Checks if the CSV headers match the dictionary keys.

        Returns:
            bool: True if the database format is valid.
        
        Raises:
            ValueError: If headers do not match the dictionary keys.
        """
        # Verify existing CSV headers match dictionary keys
        existing_field_names = self.get_existing_field_names()
        provided_field_names = list(self.dictionary.keys())
        if existing_field_names == provided_field_names:
            return True
        else:
            raise ValueError(f"[i] Existing field names do not match with "
                             f"{self.dictionary}")
