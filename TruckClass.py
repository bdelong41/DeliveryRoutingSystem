from PackageClass import Package
class Truck:
    def __init__(self, truckerName, packageManifest, local, time=8, mileage=18):

        """ Truck takes a truckerName, package list, address, beginning
       time, and mileage as arguments. All truck statistics are 
       contained inside Truck and referenced where needed. truckManifest
       acts as a queue, packages are enqueued into the truckManifest 
       during loading. Packages are dequeued from truckManifest during
       a Delivery."""
        self.driverName = truckerName #Truckers Name 
        self.truckManifest = packageManifest #list of package objects the trucker will transport
        #self.depot = hubAddress
        self.currentLocal = local #Records the trucks current location recorded at each drop off
        #Used in lieu of referencing a package in the hash table, the time the last package was 
        #delivered is stored locally 
        self.internalTime = time #Records the time the last package was dropped off
        #used for referencing outside of truck
        self.mileage = mileage#Records the maximum number of miles the truck can move per given amount of time
        self.timeOfNextDropOff = time#Predicts the time the next package will be dropped off
        self.lastDeliveredPackage = None#Stored all package relavent data about the previous package dropped off
       #Since lastDeliveredPackage is an outdated version of the package that already exists within the hash table
       #internalTime also tracks the delivery time for lastDeliveredPackage
       #totalDistance tracks the current amount of distance the truck has travelled 
        self.totalDistance = 0
    #data Retrieval methods
    def get_trucker_name(self):
        return self.driverName
    def get_manifest(self):
        return self.truckManifest
    def get_current_local(self):
        return self.currentLocal
    def get_last_drop_off_time(self):
        return self.internalTime
    def get_time_of_next_drop_off(self):
        return self.timeOfNextDropOff
    def get_last_delivered_package(self):
        return self.lastDeliveredPackage
    def get_total_distance(self):
        return self.totalDistance
    def get_internal_time(self):
        return self.internalTime

    #data alteration methods
    #returning package being dequeued
    def get_next_package_drop_off(self):

        """ This function dequeues Package objects and returns them for 
        reference. Using timeOfNextDropOff the function determines if a
        a delivery can be met on time. Packages delivered late require 
        the user to dismiss the error."""
        if len(self.truckManifest) != 0:# O(p) p=# of delivery points
                #extracting the 
                package = self.truckManifest[0]
                if package["DeliveryDeadline"] != "EOD":
                    #this is an absolute failure case as all packages must be delivered on time
                    #During this packages are still delivered
                    if self.timeOfNextDropOff > package["ConvertedTime"] + 1/60:#1/60 places package delivery within one minute error margine
                        print("=============Failed=to=Deliver=on=Time=============")
                        print(self.timeOfNextDropOff, " ", package["ConvertedTime"], " ", package["ID"])
                        print(self.driverName)
                        input("Press enter to continue")

                #calculating distance between drop offs
                distance = float(package.lookup_distance(self.currentLocal)[1])# O(p)
                #Recording the total distance travelled
                self.totalDistance += distance
                #recording the time of current drop off
                self.internalTime = self.internalTime + distance/self.mileage
                #updating currentLocal to packages delivery address
                self.currentLocal = package["Address"]
                #Duplicating the delivered package for reference
                self.lastDeliveredPackage = package

                #Predicting the time of the next drop off
                #If there is only one package left to deliver there is 
                #not a future delivery until the truck is reloded
                if len(self.truckManifest) >= 2:
                    self.timeOfNextDropOff = self.internalTime + float(self.truckManifest[1].lookup_distance(package["Address"])[1])/self.mileage# O(p) p=#number of delivery points
                return self.truckManifest.pop(0)#returning the delivered Package
        #Indicates failure case
        return None
   
    def set_trucker_name(self, newTruckerName):
        self.SetTruckerName = newTruckerName        
    def set_manifest(self, packageList, beginningTime = 8):

        """ This function takes a list and float as argument and sets.
        truckManifest to the list input. The float input beginningTime
        is used to determine the time the first package of the queue
        will be delivered and stores it in timeOfNextDropOff."""
        self.truckManifest = packageList

        #if truckManifest is set
        if len(self.truckManifest) > 0:
            #calcuating time of drop off for the first package
            self.timeOfNextDropOff = beginningTime + float(self.truckManifest[0].lookup_distance(self.currentLocal)[1])/self.mileage

    def set_time_of_next_drop_off(self,value):

        """ This function allows the user to manually set 
        timeOfNextDropOff manually using a string input."""
        self.timeOfNextDropOff = value

    def set_current_local(self, value):

        """ This function allows currentLocal to be set manually using 
         as string input"""
        self.currentLocal = value

