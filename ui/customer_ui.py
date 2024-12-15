from domain.person import Person
from domain.company import Company
from domain.customer import Customer
from helpers.ui import UI
from helpers.validate import Validate
from ui.person_ui import PersonUI
from ui.company_ui import CompanyUI

class CustomerUI:
    """
    Manages customer-related operations such as adding, updating, and deleting
    companies or persons.

    Methods:
        add_customer(): Adds a new customer (person or company).
        delete_customer(): Deletes an existing customer.
        update_customer(): Updates details of an existing customer.
        get_customer_menu(user_name): Displays a menu to manage customers.
    """

    def add_customer(self) -> None:
        """
        Adds a new customer (either a company or a private individual).
        """
        while True:
            user_input = input("[i] Customer type: C for company and P for private: ")
            if Validate.user_entry(user_input, "cp"):  # Validate customer type
                break

        match user_input.lower():
            case "c":  # Add a company
                UI.decorate_header("New Company", with_footer_fill=True)
                company = CompanyUI().collect_data(is_updating=False)
                company.add()  # Save the new company
                UI.decorate_header("Company added", with_footer_fill=True)
            case "p":  # Add a person
                UI.decorate_header("New Person", with_footer_fill=True)
                person = PersonUI().collect_data(is_user=False, is_updating=False)
                person.add()  # Save the new person
                UI.decorate_header("Person added", with_footer_fill=True)

    def delete_customer(self) -> None:
        """
        Deletes an existing customer (either a company or a private individual).
        """
        while True:
            menu_choice = input("[i] Customer type: C for company and P for private: ")
            if Validate.user_entry(menu_choice, "cp"):  # Validate customer type
                break

        match menu_choice.lower():
            case "c":  # Delete a company
                customer_id = input("[i] Company id: ")
                company = Company(customer_id)
                company.delete()  # Delete the company record
            case "p":  # Delete a person
                customer_id = input("[i] Person id: ")
                person = Person(customer_id)
                person.delete()  # Delete the person record

    def update_customer(self) -> None:
        """
        Updates details of an existing customer (either a company or a person).
        """
        while True:
            user_input = input("[i] Customer type: C for company and P for private: ")
            if Validate.user_entry(user_input, "cp"):  # Validate customer type
                break

        match user_input.lower():
            case "c":  # Update a company
                while True:
                    user_input = input("[i] Company id: ")
                    if user_input.lower() == "c":  # Allow cancellation
                        break
                    company_exists = Company(user_input).find()
                    if company_exists:  # Check if the company exists
                        UI.decorate_header("Update Company", with_footer_fill=True)
                        company = CompanyUI().collect_data(is_updating=True)
                        company.id = user_input  # Retain original ID
                        company.update()  # Save updated details
                        UI.decorate_header("Company updated", with_footer_fill=True)
                        break
                    else:
                        print("[i] Company not found, please try again or (C)ancel")
            case "p":  # Update a person
                while True:
                    user_input = input("[i] Person id: ")
                    if user_input.lower() == "c":  # Allow cancellation
                        break
                    existing_person = Person(user_input)
                    person_exists = existing_person.find()
                    if person_exists:  # Check if the person exists
                        UI.decorate_header("Update Person", with_footer_fill=True)
                        person = PersonUI().collect_data(is_user=existing_person.is_user, is_updating=True)
                        person.id = user_input  # Retain original ID
                        person.update()  # Save updated details
                        UI.decorate_header("Person updated", with_footer_fill=True)
                        break
                    else:
                        print("[i] Person not found, please try again or (C)ancel")

    def get_customer_menu(self, user_name: str) -> None:
        """
        Displays a menu for managing customers, allowing the user to add,
        update, or delete a customer.

        Args:
            user_name (str): The name of the current user.
        """
        UI.decorate_header(
            "(A)dd (U)pdate (D)elete", user_name=user_name, with_footer_fill=True
        )

        while True:
            user_input = input(
                "Please choose A to add a customer, U to update a customer, "
                "or D to delete a customer: "
            )
            if Validate.user_entry(user_input, "aud"):  # Validate menu choice
                break

        customer = CustomerUI()
        match user_input.lower():
            case "a":  # Add a customer
                customer.add_customer()
            case "u":  # Update a customer
                customer.update_customer()
            case "d":  # Delete a customer
                customer.delete_customer()
