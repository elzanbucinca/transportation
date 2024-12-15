from ui.main_ui import MainUI

if __name__ == "__main__":
    """
    Entry point of the application.
    Initializes the main user interface and starts the program flow.
    """
    main_ui = MainUI()  # Create an instance of the MainUI class
    main_ui.get_user()  # Authenticate or register the user
    main_ui.get_main_menu()  # Display and handle the main menu options