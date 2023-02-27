from NodeClass import Node 
import copy
class Package:

    """ Package class is another object with dictionary functionalities 
    used to conceptualize actual packages. Each Package Object contains
    an ID, weight, exception information, as well as current status 
    information. Delivery information is included in city, deliveryInfo, 
    delivDeadline, and timeOfDelivery. Each Package object has a Node 
    used to store destination information as well as distances making 
    it easier to compare and find distances between Nodes. nodeList
    allows a Package object to contain distance information"""
    #Main initialization function
    def __init__ (self, packageID, deliveryAddress, deliveryCity, deliveryState, deliveryZip, deliveryDeadline, packageWeight, specialNotes, nodeList, packageStatus="At Local Carrier Facility"):
        self.id = str.strip(packageID).replace(" ", "")
        self.city = str.strip(deliveryCity).replace(" ", "")
        self.deliveryInfo = Node(deliveryAddress, deliveryZip, deliveryState)#DeliveryInfo includes the delivery node
        self.delivDeadline = str.strip(deliveryDeadline).replace(" ", "")
        self.weight = str.strip(packageWeight).replace(" ", "")
        self.notes = str.strip(specialNotes).replace(" ", "")
        self.status = packageStatus#is by default At Local Carrier Facility
        self.exception = None
        self.convertedTime = 0# delivery deadline converted into a 24hr format stored as float data for easy comparison
        self.timeOfDelivery = 0# records actual time package is delivered
        #Package status has four options
            #En Rout To Carrier Facility
            #At Local Carrier Facility
            #En Rout
            #Delivered

        #converting time to 24hour
        convertingTime = self.delivDeadline
        convertedHour = 0
        convertedMinutes = 0
        hour = ""
        minutes = ""
        ampm = ""
        time = None

        #Converting Timely packages deliveryDeadline to a 24hr format
        #This is done during initialization to reduce runtime complexity
        #Preventing 
        if convertingTime != "EOD" and convertingTime != None:
            for n in range(0, len(convertingTime)):
                if convertingTime[n] == ":":
                    hour = convertingTime[0:n]
                    minutes = convertingTime[n + 1:n + 3]
            ampm = convertingTime[len(convertingTime) - 2:]
            convertedHour = int(hour)
            convertedMinutes = float(minutes)/60 
            if ampm == "pm":
                convertedHour = convertedHour + 12.0
        
            time = float(convertedHour) + float(convertedMinutes)#storing as float data
            self.convertedTime = time
        
        #generating Exception data
        for counter in range(0, len(self.notes)):
            if self.notes[counter: len(self.notes) - 1] == "Canonlybeontruck":
                truckNumber = self.notes[counter + 16]
                self.exception = ("Truck", truckNumber)
            elif self.notes[counter: len(self.notes) - 6] == "Delayedonflight---willnotarrivetodepotuntil":
                newTime = self.notes[counter + len(self.notes) - 6:]
                self.exception = ("Delayed", newTime)
                self.status = "En Rout To Carrier Facility"
            elif self.notes[counter:] == "Wrongaddresslisted":
                timeUpdated = None#timeUpdated stores the time it was updated for reference
                self.exception = ("WrongAddress", 0, timeUpdated)
                if self.notes[counter: counter + 19] == "Mustbedeliveredwith":
                    packageIDList = []
                    sentence = ""

                    for counter2 in range(counter + 19, len(self.notes)):
                        if counter2 == len(self.notes) - 1:
                            packageIDList.append(sentence)
                        elif self.notes[counter2] == ",":
                            packageIDList.append(sentence)
                            sentence = ""
                        elif ord(self.notes[counter2]) >= 48 and ord(self.notes[counter2]) <= 57:
                            sentence = sentence + self.notes[counter2]

                    self.exception = ("GroupDelivery", packageIDList)
        #resetting deliveryInfo to a pre-existing Node object
        for index in range(0, len(nodeList)):
            #using the == operator overloaded in Node class
            if nodeList[index] == self.deliveryInfo:
                self.deliveryInfo = nodeList[index]#copies over all Node distance information
                return None       
            


#Data retrieval methods
    #providing regular functions in lew of brackets
    def get_id(self):
        return self.id
    def get_delivery_address(self):
        return self.deliveryInfo.get_address()
    def get_delivery_deadline(self):
        return self.delivDeadline
    def get_delivery_city(self):
        return self.city
    def get_delivery_zip(self):
        return self.deliveryInfo.get_zip()
    def get_package_weight(self):
        return self.weight
    #Status Records Current Delivery information in transit, delivered, delayed
    def get_package_status(self):
        return self.status
    def get_special_notes(self):
        return self.notes
    def get_delivery_state(self):
        return self.deliveryInfo.get_state()
    def get_exceptions(self):
        return self.exception
    


    #Dictionary functionality using operator overloading
    def __getitem__(self, item):
        if item == "ID":
            return self.id
        if item == "Address":
            return self.deliveryInfo["Address"]
        if item == "City":
            return self.city
        if item == "Zip":
            return self.deliveryInfo["Zip"]
        if item == "DeliveryInfo":
            return self.deliveryInfo
        if item == "State":
            return self.deliveryInfo["State"]
        if item == "DeliveryDeadline":
            return self.delivDeadline
        if item == "Weight":
            return self.weight
        if item == "Notes":
            return self.notes
        if item == "Status":
            return self.status
        if item == "DistanceRange":
            return self.deliveryInfo.distanceRange
        if item == "Exceptions":
            return self.exception
        if item == "ConvertedTime":
            return self.convertedTime
        if item == "TimeOfDelivery":
            return self.timeOfDelivery
        if item == "DeliveryInfo":
            return self.deliverInfo
    def lookup_distance(self, address):
        return self.deliveryInfo.get_distance(address)

#Member Alteration Functions

    #Dictionary functionality using operator overloading
    def __setitem__(self, item, value):
        if item == "Address":
            self.deliveryInfo["Address"] = value
        if item == "City":
            self.city = value
        if item == "Zip":
            self.deliveryInfo["Zip"] = value
        if item == "State":
            self.deliveryInfo["State"] = value
        if item == "DeliveryDeadline":
            self.delivDeadline = value
        if item == "Weight":
            self.weight = value
        if item == "Notes":
            self.notes = value
        if item == "Status":
            self.status = value
        if item == "Exceptions":
            self.exception = value
        if item == "TimeOfDelivery":
            self.timeOfDelivery = value
        if item == "DeliveryInfo":
            self.deliveryInfo = value
    #providing regular functions in lew of brackets
    def set_id(self, packageID):
        self.id = packageID
    def set_delivery_address(self, deliveryAddress):
        self.deliveryInfo.set_address(deliveryAddress)
    def set_dilivery_deadline(self, deliveryDeadline):
        self.delivDeadline = deliveryDeadline
    def set_delivery_city(self, deliveryCity):
        self.deliveryInfo.set_city_local(deliveryCity)
    def set_delivery_zip(self, deliveryZip):
        self.deliveryInfo.set_zip(deliveryZip)
    def set_weight(self, packageWeight):
        self.weight = packageWeight
    def alter_status(self, packageStatus):
        self.status = packageStatus
    def alter_notes(self, specialNotes):
        self.notes = specialNotes
    def set_exception(self, tuple):
        self.exception = tuple