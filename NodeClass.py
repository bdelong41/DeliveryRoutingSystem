class Node:
    """
    Node acts as a dictinoary object used to conceptualize
    actual delivery points. Each Node contains an address, zip, 
    state that it's in as well as distance statistics relative to 
    other delivery points. Each distance statistic can be accessed by 
    providing a reference address. distanceRange is by defualt an empty 
    list. Overloading the bracket opperators provides Node objects 
    Dictionary functionality."""
    def __init__(self, deliveryAddress, zipCode, deliveryState):
        self.address = str.strip(deliveryAddress).replace(" ", "")
        self.zip = str.strip(zipCode).replace(" ", "")
        self.state = str.strip(deliveryState).replace(" ", "")
        self.distanceRange = []#disatnceRange makes it simpler to find a distance between two Nodes


#data Retrieval Methods
    def get_address(self):
        return self.address
    def get_zip(self):
        return self.zip
    def get_state(self):
        return self.state
    #adding dictinary functionality
    def __getitem__(self, item):
        if item == "Address":
            return self.address
        if item == "State":
            return self.state
        if item == "Zip":
            return self.zip
        if item == "DistanceRange":
            return self.distanceRange

    def get_distance(self, addressInput):

        """This function retrieves the distance between this Node and
        another Node by using a reference address ad input"""
        for index in range(0, len(self.distanceRange)):
            distanceNode = self.distanceRange[index]
            if self.distanceRange[index][0].replace(" ","") == addressInput.replace(" ",""):
                return self.distanceRange[index]
        return 0

    def __eq__(self, other):
        """Allowing other Node objects to be comparable using the 
        equality opperator"""
        if self.address == other.get_address():
            if self.zip == other.get_zip():
                #if self.State == other.GetState():
                return True
        return False

#Data Alteration Methods
    def set_address(self, newAddress):
        self.address = SetAddress
    def set_city_local(self, newCityLocal):
        self.City = newCityLocal
    def set_zip(self, newZipCode):
        self.zip = newZipCode
    def add_distance_range(self, value):
        self.distanceRange.append(value)
    def __setitem__(self, item, value):
        if item == "Address":
            self.address = value
        if item == "City":
            self.City = value
        if item == "Zip":
            self.zip = value
        if item == "State":
            self.state = value


