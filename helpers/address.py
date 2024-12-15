"""
This Module presents Address Class
"""

class Address:
    """This class create an address object has attributes
    @ street_name : str
    --------------
    @ building_number: str
    ------------------
    @ zip_code : str
    ----------
    @ city: str
    ---------
    @ country : str
    ----------
    """

    def __init__(self, street_name:str = None,
                 building_number:int = None,
                 zip_code:int = None,
                 city:str = None,
                 country:str = None) -> None:
        self.street_name = street_name
        self.building_number = building_number
        self.zip_code = zip_code
        self.city = city
        self.country = country

    def __repr__(self) -> str:
        return f"""
        \n###### Here is address info #######
        Street Name = {self.street_name}
        Building Number = {self.building_number}
        Zip Code = {self.zip_code}
        City = {self.city}
        Country = {self.country}
        ####################################
        """
    
    def print_address(self):
        """
        Method that print to terminal our address using __repr__
        """
        print(self)
    
    def change_address(self,street_name = "1",
                 building_number = 1,
                 zip_code = 1,
                 city="1",
                 country = "1") -> None:
        """
        This method will change the attribute value in our instance
        that get new value from user code        
        """
        if street_name !="1":
            self.street_name = street_name
            print(f"[debug] : street_name changed to {self.street_name}")
        if building_number != 1:
            self.building_number = building_number
            print(f"[debug] : Building_number changed to {self.building_number}")
        if zip_code !=1:
            self.zip_code = zip_code
            print(f"[debug] : Zip_code change to {self.zip_code}")
        if city !="1":
            self.city = city
            print(f"[debug] : City  change to {self.city}")
        if country !="1":
            self.country = country
            print(f"[debug] : Country  change to {self.country}")

    def get_address_from_dictionary(self,address:dict):
        """Method that create instance of our class Address based on
        instance we created already.
        Note: we shall discuss class methods soon
        """
        self.__init__(street_name=address["street_name"],
                      building_number=address["building_number"],
                      zip_code=address["zip_code"],
                      city=address["city"],
                      country=address["country"])
        return self
    

    def set_addresss(self):
        print("==== Address ====")
        street_name = input("[i] Please enter street name: ")
        building_number = input("[i] Please enter building number: ")
        zip_code = input("[i] Please enter zip code: ")
        city = input("[i] Please enter city: ")
        address = Address(  street_name=street_name, 
                            building_number=building_number,
                            zip_code=zip_code,
                            city=city,
                            country="Sweden"
                        )
        print("========================")
        return address.__dict__
    
    def export_to_dict(self):
        return self.__dict__