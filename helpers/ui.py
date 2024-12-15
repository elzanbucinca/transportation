import os

class UI:
    """
    A utility class for rendering decorated headers in the terminal UI.

    Methods:
        decorate_header(text, width, fill_char, user_name, with_footer_fill):
            Clears the terminal and displays a formatted header with optional
            user-specific text and footer decoration.
    """

    @staticmethod
    def decorate_header(text, width=120, fill_char="=", user_name=None, 
                        with_footer_fill=False):
        """
        Clears the terminal and displays a formatted header.

        Args:
            text (str): The main text to display in the header.
            width (int): Total width of the header. Default is 120.
            fill_char (str): Character used for the header borders. Default is "=".
            user_name (str, optional): Name of the user to include in the header.
            with_footer_fill (bool): Whether to add a footer line. Default is False.
        """
        # Clear the terminal screen for a clean header display
        os.system('cls' if os.name == 'nt' else 'clear')

        # Padding and content width calculations
        padding = fill_char * 4  # Creates the decorative padding
        content_width = width - len(padding) * 2  # Adjust content for padding

        # Center-align the main header text
        centered_text = text.center(content_width)

        # Display top border
        print(fill_char * width)

        # Construct and center-align the welcome text
        if user_name is None:
            welcome_text = "Welcome to TRANSPORTER"
        else:
            welcome_text = f"TRANSPORTER - User: {user_name}"
        centered_welcome = welcome_text.center(content_width)
        print(f"{padding}{centered_welcome}{padding}")

        # Display divider line
        print(fill_char * width)

        # Display the main header text
        print(f"{padding}{centered_text}{padding}")

        # Optionally add a footer border line
        if with_footer_fill:
            print(fill_char * width)
