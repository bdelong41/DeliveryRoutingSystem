from PackageClass import Package
import copy
#from TruckClass import Truck

#The Hash Table stores package objects according to address location
class HashTable(Package):

    """ HathTable stores Packages added into it. Packages can be added 
    linearly (appended to the end of table) if it has a unique address.
    Using a double hashing algorithm using zip and address. Empty 
    Buckets are indicated by an empty list."""
    def __init__(self, newPackage): #O(c) where c is the number of characters in addressValue and zipValue
        #initializing table to an empty list
        self.table = [[]]*20 #initializing that table length to 20
        address = newPackage["Address"] 
        zip = newPackage["Zip"]
        addressValue = 0
        zipValue = 0
        
        #O(n) n = number of terms within address
        #converting address type string to an ascii value
        for n in address:
            addressValue += ord(n)
        #0(n) n = number of terms within zip
        #converting zip type string to an ascii value		
        for n in zip:
            zipValue += ord(n)
            
        #generating hash code
        hash = (addressValue * zipValue) % 20
        
        #initializing empty bucket to list
        self.table[hash] = [newPackage]

    def convert_time(self, time):

        """ This function takes a string input and returns a float. 
        A 12 hour format time is entered in and a 24 hour format time is 
        returned."""
        convertedHour = 0#stores hours out of 24
        convertedMinutes = 0#stores minutes as tenths instead of 60'ths
        hour = ""#stores hour portion of the string
        minutes = ""#stores minutes portion of the string
        ampm = ""#stores time of day

        #ignoring non 12 hr time formats
        if time == "EOD" or time == None:
            return 0
        #Traversing the 12 hr time for a delimiter
        for n in range(0, len(time)):
            if time[n] == ":":# Detecting the delimiter
                hour = time[0:n]#slicing the string from index 0 to delimiter
                minutes = time[n + 1:n + 3]#slicing from the delimiter to the time of day indicator
        ampm = time[len(time) - 2:]#extracting the last 2 indecies which record time of day
        convertedHour = float(hour)#Casting hour as a float
        convertedMinutes = float(minutes)#Casting minutes as a float
        #Accounting for time of day
        if ampm == "PM":
            #adding 12 hrs for time of day being pm
            convertedHour = convertedHour + 12.0     
        #adding the converted times and rounding the result to two decimal places
        convertedTime = round(float(convertedHour) + float(convertedMinutes)/60, 2)
        return convertedTime

#Data retrieval methods
    #displays the statistics of each package stored in the hash table
    def print_hash(self):
        for n in range(0, 20):
            for index in range(0, len(self.table[n])):
                package1 = self.table[n][index]#extracting package object

                #displaying package objects stats
                print("ID: ", package1["ID"])
                print("Address: ", package1["Address"])
                print("Deadline: ", package1["DeliveryDeadline"])
                print("City: ", package1["City"])
                print("State: ", package1["State"])
                print("Zip: ", package1["Zip"])
                print("Weight: ", package1["Weight"])
                print("Notes: ", package1["Notes"])
                print("Exceptions: ", package1["Exceptions"])
                print("Status: ", package1["Status"])
                print("Time of Delivery: ", package1["TimeOfDelivery"])
                
                print()#Spacer

    def get_package_using_id(self, id):# O(h)

        """" This searches linearly through the hash table until a 
        package object with same id is found. Function completes once
        the entire table is traversed. If no packages are found
        the function returns None """

        package = None
        for index in range(0, 20):# O(20)
            for counter in range(0, len(self.table[index])):# O(h) h= number of packages in hash
                if self.table[index][counter]["ID"] == id:
                    package = self.table[index][counter]
        return package

    def get_package_using_address(self, referenceAddress): #O(h)

        """" This searches linearly through the hash table for Packages
        with the same address. Packages with the same address are 
        appended to packageList and then returned once the entire table 
        is traversed. If no Packages are found the function returns an 
        empty list """
        packageList = []
        for index in range(0, 20):
            for counter in range(0, len(self.table[index])):
                if (referenceAddress == self.table[index][counter]["Address"]):
                    packageList.append(self.table[index][counter])
        return packageList

    
    def get_package_using_status(self, status):

        """" This searches linearly through the hash table for packages
        with the same status. Packages with the same status are 
        appended to packageList and then returned once the entire table 
        is traversed. If no Packages are found the function returns an 
        empty list """
        packageList = []
        for index in range(0, len(self.table)):
            for counter in range(0, len(self.table)):
                if status == self.table[index][counter].GetPackageStatus():
                    packageList.append(self.table[index][counter])
        return packageList
    
    def get_package_using_weight(self, weight):

        """" This searches linearly through the hash table for packages
        with the same status. Packages with the same weight are 
        appended to packageList and then returned once the entire table 
        is traversed. function completes once the the entire table is
        traversed. If no Packages are found the function returns an 
        empty list """
        packageList = []
        for index in range(0, len(self.table)):
            for counter in range(0, len(self.table)):
                if weight == self.table[index][counter].GetPackageWeight():
                    packageList.append(self.table[index][counter])
        return packageList

    def get_package_using_deadline(self, deadline):

        """" This searches linearly through the hash table for packages
        with the same status. Packages with the same deadline are 
        appended to packageList and then returned once the entire table 
        is traversed. function completes once the the entire table is
        traversed. If no Packages are found the function returns an 
        empty list """
        packageList = []
        for index in range(0, len(self.table)):
            for counter in range(0, len(self.table)):
                if deadline == self.table[index][counter].GetDeliveryDeadline():
                    packageList.append(self.table[index][counter])
        return packagelist

    def get_package_using_city(self, city):

        """" This searches linearly through the hash table for packages
        with the same status. Packages with the same delivery city are 
        appended to packageList and then returned once the entire table 
        is traversed. function completes once the the entire table is
        traversed. If no Packages are found the function returns an 
        empty list """
        packageList = []
        for index in range(0, len(self.table)):
            for counter in range(0, len(self.table)):
                if city == self.table[index][counter].GetDeliveryCity():
                    packageList.append(self.table[index][counter])
        return Packagelist

    def get_package_using_zip(self, zip):

        """" This searches linearly through the hash table for packages
        with the same status. Packages with the same delivery zip are 
        appended to packageList and then returned once the entire table 
        is traversed. function completes once the the entire table is
        traversed. If no Packages are found the function returns an 
        empty list """
        PackageList = []
        for index in range(0, len(self.table)):
            for counter in range(0, len(self.table)):
                if zip == self.table[index][counter].GetDeliveryZip():
                    packageList.append(self.table[index][counter])
        return packagelist

    def get_package_using_zip_address(self, zip, address, id):

        """This function generates a hash code using zip and address, 
        and then searches the table for a package with the same id.
        Traversal begins at the hash index and terminates when either
        the package is found or the table has been completly traversed. """
        addressValue = 0
        zipValue = 0

        #converting address type string to decimal alias
        for n in address:
            #summing the decimal aliases
            addressValue += ord(n)
        #converting zip type string to decimal alias
        for n in zip:
            #summing the decimal aliases
            zipValue += ord(n)
            
        #generating hash code
        hash = (addressValue * zipValue) % 20

        #searching through the table starting at the hash index
        for index in range(hash, len(self.table)):
            for counter in range(0, len(self.table[index])):
                package = self.table[index][counter]
                #comparing package ID with id
                if package["ID"] == id:
                    return package
        #case: specified package doesnot exist
        return 0

    def get_package_using_params(self, packageID, address, deadline, city, zip, weight, status):# O(c + n) where c=#number of characters stored in address and zip
        
        """ This functions retrieves a package by matching the given 
        parameters against each pacakge in the table. Since the user 
        input doesnot include a zip specification a hash code 
        cannot be generated and the hash table must be searched 
        starting from index 0"""

        addressValue = 0
        zipValue = 0

        #converting address type string to decimal alias
        for n in address:
            #summing the decimal aliases
            addressValue += ord(n)
        #converting zip type string to decimal alias
        for n in zip:
            #summing the decimal aliases
            zipValue += ord(n)
        #generating hash code
        hash = (addressValue * zipValue) % 20

        #searching packages at the hash index
        for counter in range(0, len(self.table[hash])):# O(n)
            package = self.table[hash][counter]
            if package["Address"] == address:           
                if package["City"] == city:
                    package = self.table[hash][counter]
                    if package["Status"] == status:
                        if package["DeliveryDeadline"] == deadline:
                            if package["Weight"] == weight:
                                if package["ID"] == packageID:
                                    return package
                                         
        return 0

    def is_not_in(self, package, list):

        """This function takes a Package object and list as input and 
        determines if the Package doesnot exist inside the list. Returns
        False if it already exist and returns True if the Package is 
        unique to list."""
        for index in range(0, len(list)):
            if list[index]["ID"] == package["ID"]:
                return False           
        return True

    def throw_package_with_earliest_time(self, state, packageList):#O(h**2)

        """" This takes a string and list as arguments and returns a 
        package with the earliest deadline with respect to the list 
        argument. Packages who's status is not At Local Carrier Facility
        are excluded as well as End of Day deadlines. Only same State 
        packages are included. Packages that already exist in 
        packageList are excluded as well. Function terminates once the
        entire table has been explored."""
        leastTimePackage = None
        for index in range(0, 20):#O(20)
            for counter in range(0, len(self.table[index])): #O(20h(h/2))
                currentPackage = self.table[index][counter]
                if currentPackage["State"] != state:#ignoring packages not in the same state
                    continue
                #ignoring delivered pacakges and packages being delivered
                if currentPackage["Status"] != "At Local Carrier Facility":
                    continue
                #ignoring packages that are already present in PackageList
                if not self.is_not_in(currentPackage, packageList): # O(i)
                    continue
                #Excluding EOD packages
                if currentPackage["DeliveryDeadline"] == "EOD":
                    continue
                #initializing leastTimePacakge
                elif leastTimePackage == None:
                    leastTimePackage = currentPackage
                #setting leastTimePackage to a package with an earlier
                #deadline
                elif currentPackage["ConvertedTime"] < leastTimePackage["ConvertedTime"]:
                    leastTimePackage = currentPackage

        return leastTimePackage

    def least_distance(self, packageList):# O(n**3)

        """ This function takes a list of packages as input and creates a Queue.
        The pacakage with the least distance with respect to the tails
        of the Queue is added to the tail. The Queue is returned once
        all packages from sortedList is added. The first element of 
        sortedList is used to initialize the Queue.
        """ 
        queue = [packageList[0]]

        #Tracks the least distant package with respect to the tail of the queue
        leastDistancePackage = None

        head = queue[0]
        queue.append(head)
        for counter1 in range(0, len(packageList)):# O(n**2((n)/2 + 2p)) = (1/2)(n**3) + 2pn**2
            for counter in range(0, len(packageList)):# O(n(n)/2 + 2p)) n = #of packages in packageList p=#of delivery points
                package = packageList[counter]
                if package["ID"] == head["ID"]:#preventing package from refrencing itself
                    continue

                #excluding packages that already exist in queue
                #this guarentees that a package that already exists in 
                #queue is not used
                elif not self.is_not_in(package, queue):# O(i) where i is the number of elements in queue
                    continue

                #if leastDistancePackage is not initialized
                elif leastDistancePackage == None:
                    #initializing leastDistancePackage
                    leastDistancePackage = package
                    #continuing after package is used to initialize 
                    #leastDistancePackage
                    continue

                #distance comparison, least distant package is selected 
                else:
                    #head package's address is referenced when looking up distance
                    distance1 = float(package.lookup_distance(head["Address"])[1])# O(p)
                    distance2 = float(leastDistancePackage.lookup_distance(head["Address"])[1])# O(p)
                    if distance1 <= distance2:
                        leastDistancePackage = package
            #adding the least distant package to queue
            queue.append(leastDistancePackage)
            #setting head to the queue's head
            head = queue[len(queue) - 1]
        #returning queue
        return queue

    def gather_delayed_packages(self):# O(h) h is the number of packages stored in hash table

        """ This functions searches for packages that are delayed
        and stores them into a list. Function completes once the entire
        table has been explored."""

        packageList = []
        #traversing through the table columns
        for index in range(0, 20):
            #traversing through the table rows
            for counter in range(0, len(self.table[index])):
                #eliminating packages that do not have exceptions
                if self.table[index][counter]["Exceptions"] == None:
                    continue
                #eliminating packages with exceptions who's status is 
                #not En Rout To Carrier Facility
                elif self.table[index][counter]["Status"] == "En Rout To Carrier Facility":
                    #excepting pacakges that are delayed
                    if self.table[index][counter]["Exceptions"][0] == "Delayed":
                        #adding package to packageList
                        packageList.append(self.table[index][counter])

        return packageList
    
    def gather_exception_packages(self):#O(gh**2) where h is the number of packages stored in hash g = the number pckgs in a group delivs which is at worst the length of hash
    
        """ This function searches for packages that have to be 
        deliverd with specific packages or can only be delivered
        on a specific truck. For the group delivery exception 
        all packages that are included in the group delivery are 
        returned as well. Returns a tuple of lists. Function 
        terminates once the entire hash table has been explored.
        """
        groupDeliveryList=[]
        truckExceptionList=[]
        for index in range(0, len(self.table)):# O(20)
            for counter in range(0, len(self.table[index])): #O(20h)
                package=self.table[index][counter]
                #ignoring packages that are not at the carrier facility
                if package["Status"] != "At Local Carrier Facility" or package["Status"]:
                    continue
                if package["Exceptions"]!=None:
                    #extracting package's exception data
                    exception=package["Exceptions"]
                    #Case exception data is a groupDelivery
                    if exception[0]=="GroupDelivery":
                        groupDeliveryList.append([package])
                        #retrieving packages part of a group delivery
                        #g can contain the id of every pckg in hash
                        for n in range(0, len(exception[1])):# O(gh) g= amount of pckgs in each group
                            #gathering packages that are part of a group delivery
                            groupPackage=self.get_package_using_id(exception[1][n])# O(h)
                            if groupPackage!=None:
                                groupDeliveryList[len(groupDeliveryList)-1].append(groupPackage)
                    #Case truck number exceptions
                    elif exception[0]=="Truck":
                        truckExceptionList.append(package)
        #returning groupDeliveryList and truckExceptionList as a tuple
        return (groupDeliveryList,truckExceptionList)

    def gather_eod_package(self):#O(h)
    
        """ This function gathers packages with a delivery deadline of 
        End Of Day and stores them into a list. Packages that have been
        delivered or are not at the carrier facility are ignored. 
        Function completes once the entire table has been explored."""
        packageList = []
        for index in range(0, 20):# constant since hash is 20
            for counter in range(0, len(self.table[index])):# O(h)
                package = self.table[index][counter]

                if package["Exceptions"] != None:
                    #ignoring wrong address packages that have not been updated
                    if package["Exceptions"][0] == "WrongAddress":
                        if package["Exceptions"][1] == 0:#0 indicated the package has not been updated
                            continue

                #Checking Status and delivery deadline
                if package["Status"] == "At Local Carrier Facility":
                    #Delivery deadline must be EOD for the package to be stored
                    if package["DeliveryDeadline"] == "EOD":
                        packageList.append(package)
        return packageList

    def count_delayed_packages(self, time):# O(h) h = # of packages in the table
    
        """ This function counts the number of pacakges who's delivery
        deadline is not EOD. Packages with exceptions are ignored.
        Function completes once the entire table has been explored"""
        none_eod_pacakges = 0
        for index in range(0, 20):
            for counter in range(0, len(self.table[index])):
                if self.table[index][counter]["Exceptions"] != None:
                    if self.table[index][counter]["Exceptions"][0] == "Delayed" and self.table[index][counter]["Status"] == "At Local Carrier Facility":
                        if self.table[index][counter]["DeliveryDeadline"] != "EOD":
                            if self.convert_time(self.table[index][counter]["Exceptions"][1]) < time:
                                none_eod_pacakges += 1
        return none_eod_pacakges

    def get_packages_not_delivered(self):# O(h)

        """ This function traverses the hash table and searches for 
        packages with a status not equal to "Delivered".
        packages found are counted. Function completes once all elements
        in the hash table have been searched."""
        packageCounter = 0
        for index in range(0, 20):
            for counter in range(0, len(self.table[index])):
                package = self.table[index][counter]
                if package["Status"] !="Delivered":
                    packageCounter += 1
        return packageCounter

#Data alteration members

    def add_sort(self, package):# O(c) c = # of characters in address and zip

        """ Takes a Package object as argument and then adds it to the
        table using a hash code. The hash code is generated using the 
        address and zip stored inside Package object. Using the empty
        bucket method if the bucket is not empty the Package object is 
        stored below the bucket. Collisions are mitigated by chaining"""
        address = package["Address"]
        zip = package["Zip"]
        addressValue = 0
        zipValue = 0
        
        #converting address type string to an ascii value
        for n in address: #
            #adding the decimal alias of each character together
            addressValue += ord(n)
        #converting zip type string to an ascii value		
        for n in zip:#
            #adding the decimal alias of each character together 
            zipValue += ord(n)

	    #generating hash code by multiplying addressValue and zipValue
        #and taking the modulo of the original size of the table
        hash = (addressValue * zipValue) % 20

        #initializing empty bucket to list
        if self.table[hash] == []:
            self.table[hash] = [package]
            return 1

		#chaining packages with the same hash code
        elif self.table[hash] != []:				
            self.table[hash].append(package)
            return 1
        
        return 0#case failure to store package

    def add_package_with_params(self, packageID, deliveryAddress, deliveryCity, deliveryDeadline, packageWeight, deliveryStatus):# O(h)
        
        """This function takes the minimum parameters for initializing 
        a Package object, initializes the Package object and then adds 
        the package to the table using the member function add_sort()"""
        #package already exists
        if self.get_package_using_id(packageID) != None:
            return 2
        #filling in missing state and zip information
        for index in range(0, 20):
            for counter in range(0, len(self.table[index])):
                package = self.table[index][counter]
                #Trying to extract the necassary information from simillar packages
                if package["Address"] == deliveryAddress and package["City"] == deliveryCity:
                    #creating package object using input and information from simillar packages
                    newPackage = Package(packageID, deliveryAddress, deliveryCity, package["State"], package["Zip"], deliveryDeadline, packageWeight," ", [package["DeliveryInfo"]], deliveryStatus )
                    if newPackage == 0:
                        return 0
                    else:
                        self.table[index].append(newPackage)
                        return 1

        return 0

    def update_hash_delivery_status(self, packageList, status):# O(nch) n=# of elements in packageList
    
        """ This function takes a List and string as arguments and 
        uses them to update the delivery status ot packages in the hash
        table. Packages within packageList are matched against packages 
        in the hash table, matches then have their status updated using 
        the status argument. Function completes once all packages 
        within pacakageList are referenced."""
        
        #traversing packageList
        for counter in range(0, len(packageList)):
            #referencing pacakge object in packageList
            referencePackage = packageList[counter]
            
            #extracting address and zip from reference
            address = referencePackage["Address"]
            zip = referencePackage["Zip"]
            
            #converting address and zip to an integer value
            addressValue = 0
            zipValue = 0

            #converting address type string to decimal 
            for n in address:
                #converting character to decimal alias and adding it to addressValue
                addressValue += ord(n)
                
            #converting zip type string to decimal 		
            for n in zip:
                #converting character to decimal alias and adding it to addressValue
                zipValue += ord(n)
                
            #generating hash code
            hashCode = (addressValue * zipValue) % 20
            
            #traversing table row at the hash index
            for index in range(0, len(self.table[hashCode])):
                package = self.table[hashCode][index]
                if package["ID"] == referencePackage["ID"]:
                    #setting status of package in the hash table
                    self.table[hashCode][index]["Status"] = status
        return 1
        
    def update_package_status(self,package, status, deliveryTime=0):# O(ch)
        """ This function takes a package object, two strings as input
        and updates the status and delivery time of the package obbject in the 
        hash table. By default the packages delivery time is not changed. 
        Function completes once either package object is found in the 
        hash table or table row at the hash index is explored."""
        
        #extracting address and zip from reference
        address = package["Address"]
        zip = package["Zip"]
            
        #converting address and zip to an integer value
        addressValue = 0
        zipValue = 0

        #converting address type string to decimal 
        for n in address:
            #converting character to decimal alias and adding it to addressValue
            addressValue += ord(n)
                
        #converting zip type string to decimal 		
        for n in zip:
            #converting character to decimal alias and adding it to addressValue
            zipValue += ord(n)
                
        #generating hash code
        hashCode = (addressValue * zipValue) % 20
            
        #exploring table row at the hash index
        for counter in range(0, len(self.table[hashCode])): 
            if self.table[hashCode][counter]["ID"] == package["ID"]:
                self.table[hashCode][counter]["Status"] = status
                self.table[hashCode][counter]["TimeOfDelivery"] = deliveryTime
                    
                #Status update succeeded
                return 1

        #Status update Failed
        return 0

    def update_package_address(self, newAddress, newStatus, packageID, time):# O(h)

        """ This function takes 3 strings as input and uses them to 
        update the address and status of a package within the hash 
        table. pacakgeID is used to identify a single package within
        the table. Function completes once either the package is found
        or the entire table is explored."""

        #looking for a reference deliveryInfo for cloning
        donerPackage = self.get_package_using_address(newAddress)[0]# O(h)
        #linear search through Hash Table
        for index in range(0, 20):
            for counter in range(0, len(self.table[index])):
                if self.table[index][counter]["ID"] == packageID:
                    package = self.table[index][counter]

                    if package["Exceptions"] != None:
                        if package["Exceptions"][0] == "WrongAddress":#wrong address package
                            if package["Exceptions"][1] == 1:#wrong address packages has already been updated
                                return 0
                            else:
                                package["Exceptions"] = ("WrongAddress", 1, time)
                    package["Address"] = newAddress
                    package["Status"] = newStatus
                    #adding doner deliveryInfo from donerPackage
                    package["DeliveryInfo"] = donerPackage["DeliveryInfo"]
                    #removing package from the table
                    self.table[index].pop(counter)
                    #reinserting the updated package into the table
                    self.add_sort(package)
                    #Case success
                    return 1
        #Case failure
        return 0