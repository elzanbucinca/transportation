"""
This Module presents Reference Person Class
"""

class ReferencePerson:
    def __init__(self, full_name:str = None,
                 country_code:str = None,
                 mobile_number:str = None,
                 email_address:str = None) -> None:
        self.full_name = full_name
        self.country_code = country_code
        self.mobile_number = mobile_number
        self.email_address = email_address

    def __repr__(self) -> str:
        return f"""
        \n###### Reference Person #######
        Full Name = {self.full_name}
        Country Code = {self.country_code}
        Mobile Number = {self.mobile_number}
        Email Address = {self.email_address}
        ####################################
        """
    
    def print_reference_person(self):
        """
        Method that print to terminal Reference Person using __repr__
        """
        print(self)
    

    def set_reference_person(self):
        print("==== Reference Person ====")
        full_name = input("[i] Full name: ")
        country_code = input("[i] Country code: ")
        mobile_number = input("[i] Mobile number: ")
        email_address = input("[i] Email address: ")
        reference_person = ReferencePerson(  full_name=full_name, 
                            country_code=country_code,
                            mobile_number=mobile_number,
                            email_address=email_address,
                        )
        print("========================")
        return reference_person.__dict__
    
