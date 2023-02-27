#Brenden DeLong
#Western Governors University
#Student ID: 000995825


from NodeClass import Node
from PackageClass import Package
from HashTable import HashTable
from TruckClass import Truck
from FileClass import File
import copy


def convert_time_to_string(time):

    """ This function takes in a float and returns a string. The user 
    enters in a 24 hour time and it's converted into a 12 hour format. 
    Time complexity is negligible as each time string is generally the 
    same length so this function has a time complexity of O(1)."""

    #records the 12 hour time
    convertedTime = 0
    minutes = time%1#capturing the remainder
    hour = round(time//1)#converting integer float to integer

    convertedMinutes = round(minutes * 60)#converting minutes from tenths to 60ths

    #adding a 0 to make 01, 02, 03
    if convertedMinutes < 10:
        convertedMinutes = "0" + str(convertedMinutes)
    #choosing a time of day and concatinating the three portions of the 12 hour format
    if hour > 12:
        convertedTime = str(hour-12) + ":" + str(convertedMinutes) + "PM"
    else:
        convertedTime = str(hour) + ":" + str(convertedMinutes) + "AM"

    #returning the 12 hour format
    return convertedTime

def convert_time(time):

    """ This function takes a string input and returns a float. 
    A 12 hour format time is entered in and a 24 hour format time is 
    returned. Time complexity is O(1)"""
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

def print_package_list(list):
    
    """ This function takes a list populated with Package Objects and 
    displays their statistics to the user."""

    for index in range(0, len(list)):
        Package = list[index]
        print("ID: ", Package["ID"])
        print("Address: ", Package["Address"])
        print("Deadline: ", Package["DeliveryDeadline"])
        print("City: ", Package["City"])
        print("State: ", Package["State"])
        print("Zip: ", Package["Zip"])
        print("Weight: ", Package["Weight"])
        print("Notes: ", Package["Notes"])
        print("Exceptions: ", Package["Exceptions"])
        print("Status: ", Package["Status"])

        #Spacer
        print()

def is_not_in(package, list):

    """ Takes a list Package object and list of Package objects as
    input and searches the list for occurences of the Package input.
    Function returns False if the same Package object is found and 
    returns True if not. This function costs O(i) i = #of elements 
    within list"""
    for index in range(0, len(list)):#O(i)
        if list[index]["ID"] == package["ID"]:
            return False           
    return True

def calculate_time(packageList, startingDestination, time=8, speed=18):

    """ Takes a list and address as input, as well as starting time and
   mileage and calculates the total time to deliver all packages stored
   in the list manifest. manifest is treated as a queue, package deliveries
   are considered in order from head to tail. This function has a cost of 
   O(p + np) where p=# of delivery points n=# of elements in packageList"""

   #records total time to deliver packages in the list
    totalTime = time
    #if manifest is empty
    if packageList == []:
        return time

    #calculates distances using reference address
    distance = packageList[0].lookup_distance(startingDestination)[1]# O(p) p=#of delivery points
    totalDistance = float(packageList[0].lookup_distance(startingDestination)[1])#initialized from head of the queue O(p)

    #Traversing the queue calculating distances between consecutive Packages
    for index in range(1, len(packageList)):# O(n)
        #calculating distances travelled using the previous package as a starting point
        totalDistance += float(packageList[index-1].lookup_distance(packageList[index]["Address"])[1])#O(p)
       
    #calculating total time using totalDistance and speed
    totalTime = (totalDistance / 18) + time#time adds the current 24 hr time
    return round(totalTime,2)

#This cuts off Packages that cannot be delivered on time
def cut_time(list, startingAddress, beginningTime = 8):

    """ This function takes a list, address and starting time as 
    arguments and returns a segmented list of packages that can be
    delivered on time. Using calculate_time cut_time cut_time
    createa a queue of packages that can be delivered on time. 
    cut_time pushes queue and startingAddress as arguments for
    calculate_time. This function has a cost of O(ip +pi**2) 
    where i= #of elements in list p=# of delivery points"""

    #queue initialized as first element of list
    queue = [list[0]]
    #traversing list adding elements to queue
    for n in range(1, len(list)):# O(i)
        #extracting element of list
        package = list[n]
        #determining is package can be delivered on time
        if round(calculate_time(queue, startingAddress), 2) <= float(package["ConvertedTime"]):#O(p + ip)
            #adding package to queue
            queue.append(package)
    return queue

def add_group_packages(groups, maxLength=16, currentTime=8):#
    
    """ This function takes a list of package lists and generates a group 
    delivery manifest. groups contains exception packages as well as 
    their package counterparts ie "must be delivered with 19, 13". 
    groups are divided into a lists.
    Once queue has been loaded with one group it is then checked
    if packages in queue that are also included in another group 
    delivery ie. packages 16 and 19 both contain the same package
    13. If a portion exists the function will add the group it 
    belongs to the manifest. This function has a cost of 
    O(km + kim**2 + kim) i= # of list items k = # of group packages
    """


    #checking if a portion exists
    def contains_portion(group, List): #O(im**2 + mi) n=list items
        for counter in range(0, len(group)):# O(m)
            if not is_not_in (group[counter], List): #O(n) n=list items
                for n in range(0, len(group)):# O(m) * O(n)=O(mi)
	                #adding only unique packages
                    if is_not_in (group[n], List):# O(i) n=list items
                        List.append(group[n])
                return (List,True)
        return (List, False)
       
    queue = []
    # O(km + knm**2 + knm) k=number of group exceptions m=grouplistlength n=manifestlength
    for index in range(0, len(groups)): #O(k) where k is the number of group packages
        if queue == []:
            #initializing Manifest
            queue = queue + groups[index] 
            continue
        else:
            #This will capture the tuple returned by containsPortion()
            doesContain = contains_portion(groups[index], queue)#Checking if a group portion exists within manifest O(im**2 + mi)
            if doesContain[1]:
                queue = (doesContain[0])
            elif len(queue) < maxLength:
                for counter in range(0, len(groups[index])): # O(i)
                    queue.append(groups[index][counter])
    return queue

def order_by_least_time(list):
    """ This function takes a list input and returns a priority queue.
    Each element is enqueue according to least distance from the last
    enqueued element.This function has a cost of O(n**3) n = number 
    of elements within list."""

    #priority queue
    packageList = []
    eodList = []
    leadingPackage = None
    #outer loop
    for counter in range(0, len(list)):#O(n**2(n/2)) = n**3 
        #nested loop
        for index in range(0, len(list)): #O(i(1+(i-1)/2)) = O(i(i/2))
            package = list[index]
            if not is_not_in(package, packageList):# O(i) i = # of items in packageList
                continue
            if not is_not_in(package, eodList):# O(i) 
                continue
            #reserving eodList to be added to the end
            if package["DeliveryDeadline"] == "EOD":
                eodList.append(package)
                continue
            #selecting a leading package to track the current 
            #earliest deadline package
            if leadingPackage == None:
                leadingPackage = package
                continue
            else:
                #comparing delivery deadlines
                if package["ConvertedTime"] < leadingPackage["ConvertedTime"]:
                    leadingPackage = package
        if leadingPackage == None:
            return packageList + eodList
        packageList.append(leadingPackage)
        leadingPackage = None
    return packageList + eodList

def sort_by_distance(list):#O(n**3 + 2p) n=list length p=delivery points
    """ This function takes a list of Package objects and sorts them by 
    least distance. Packages with the least amount of distance are at 
    the head of the queue. distance is calculated according to the tail   
    of the queue and a reference address retrieved from a comparing  
    package. This function costs O(n**3 + 2p) n=# of elements in list 
    p=# of delivery points"""

    #this stores packages according to distance
    queue = [list[0]]
    #stores the current tail of the queue
    referencePackage = queue[0]
    #used to find the package with the least distance
    leastDistancePackage = None
    #outer for loop
    for counter1 in range(0, len(list)):#O(n**2(n/2 + 2p)) = O(n**3)
        if referencePackage == None:
            referencePackage = queue[len(queue) - 1]#referencing the last package
        else:
            #inner for loop
            for counter in range(0, len(list)):#O(n(n/2 + 2p))
                #extracting element of list
                package = list[counter]
                if package["ID"] == referencePackage["ID"]:#preventing package from refrencing itself
                    continue
                elif not is_not_in(package, queue):#O(i) preventing package from being referenced against itself
                    continue
                elif leastDistancePackage == None or not is_not_in(leastDistancePackage, queue):#O(i) i=# of items in queue
                    #initializing leastDistancePackage to a new element
                    leastDistancePackage = package
                    continue
                #if not is_not_in(leastDistancePackage, queue):
                #    continue
                else:
                    #calculating distances using tail of queue as reference
                    distance1 = float(package.lookup_distance(referencePackage["Address"])[1])#O(p) p = numer of delivery points
                    distance2 = float(leastDistancePackage.lookup_distance(referencePackage["Address"])[1])#O(p)
                    #comparing the two distances
                    if distance1 <= distance2:
                        leastDistancePackage = package

            if leastDistancePackage != None:
                #Adding leastDistancePackage to queue
                queue.append(leastDistancePackage)

                #setting referencePackage to tail of queue
                referencePackage = leastDistancePackage

                #resetting leastDistancePackage
                leastDistancePackage = None
    return queue

#O(n**3) n=number of pckgs
def generate_manifest(Table, truckNumber, hubAddress, maxLoad, beginningTime):

    """ This function is the bulk of creating delivery manifests. 
    Creating deliverable manifests is the primary goal. The function 
    begins by sorting Packages by relavance. Starting with the most 
    complicated the exception packages and group packages. Packages
    that require a specific truck are added first, then the group
    delivery packages which are the most space consuming. Timely 
    packages are added next. Timely packages that cannot be delivered
    by one truck are pushed of onto the next truck or the next pickup.
    Once all timely packges are added EOD packages are then added. 
    Packages that will be delivered late are considered undeliverable
    and are ideally pushed off onto the other delivery truck. Manifest
    is treated as a queue, distances are considered by marking the tail
    as the starting point when adding other packages. Travel distance is 
    reduced by having the manifest ordered by least distance once it's 
    been created. This function has a cost of  O(t**3 + b**3 + e**3) 
    t = # of truck specific packages, b = # of timely packages, 
    e = # of eod packages."""

    #by default the manifest can only have a length of 16
    #truckManifest
    manifest = []

    #Exceptions consists of group deliveries and truck specific deliveries
    exceptions = Table.gather_exception_packages()# O(gh**2) where h=# of packages in hash g = # of packages included in group delivery
    #Gathering Group packages
    groupByPackages = exceptions[0]

    #Gathering truck specific pacakages
    truck_exceptions = exceptions[1]

    #Organizing truck_exceptions by least time
    if len(truck_exceptions) > 0:
        truck_exceptions = order_by_least_time(truck_exceptions)# O(t**3)

    #can be moved elsewhere
    #gathering EODPackages
    eodPackages = Table.gather_eod_package()# O(h)
    #adding Group Packages
    manifest = add_group_packages(groupByPackages)#O(kg + kng**2 + kng) k=#of group packages, n=manifest length, g = amount of packages included in the group

    #Adding truck Exception Data
    if exceptions[1] != []:
        #Adding Additional Exception data
        if manifest != None:
            for n in range(0, len(exceptions[1])): #O(t) t= # of truck specific packages
                if len(manifest) < maxLoad:
                    if exceptions[1][n]["Exceptions"][1] == truckNumber:
                        manifest.append(exceptions[1][n])
        manifest = sort_by_distance(manifest)#O(maxLength**3 + 2p) p = # of delivery points

    if len(manifest) == maxLoad:
        manifest = sort_by_distance(manifest)
        return manifest
   

#adding regular non eod packages based on distance from the last node in Manifest

    #Extracting data with the earliest time from the hash table
    unsortedEarliestTimePackages = []
    state="UT"
    package = Table.throw_package_with_earliest_time(state,unsortedEarliestTimePackages)# O(h**2)
    duplicateData = []
    #loop stops executing once there are no more earliest timely packages to add
    while(package != None):# O((b-1)(h**2)) b= number of timely packages 
        state="UT"
        package = Table.throw_package_with_earliest_time(state, unsortedEarliestTimePackages + duplicateData)#O(h**2)
        if package == None:
            break
        #removing Duplicate data
        if is_not_in(package, manifest):# O(maxLength)
            
            #handling wrong address packages
            if package["Exceptions"]  != None:
                if package["Exceptions"][0] == "WrongAddress":
                    # if the time the wrong address package is updated 
                    # is not less than or equal to the input beginningTime 
                    # then continue
                    if package["Exceptions"][2] > beginningTime:
                        continue
                #Comparing arrival times of delayed packages against beginningTime
                elif package["Exceptions"][0] == "Delayed":
                    if convert_time(package["Exceptions"][1]) > beginningTime:
                        continue
                

            unsortedEarliestTimePackages.append(package)
        else:
            duplicateData.append(package)
            
    if unsortedEarliestTimePackages != []:

	    #reordering packages based on Distance From eachother
        sortedEarliestTimePackages = sort_by_distance(unsortedEarliestTimePackages)#O(b**3 + 2p)

        #removing any Nodes that cannot be met on time
        #O(bp +pb**2)
        sortedEarliestTimePackages = cut_time(sortedEarliestTimePackages, sortedEarliestTimePackages[0]["Address"], beginningTime = calculate_time(manifest, hubAddress, beginningTime))

        #These EOD packages came from the group delivery
        #removing EOD Packages from Manifest
        #EOD Packages must be added at the end
        manifestEODList = []
        newManifest = []
        for n in range(0, len(manifest)):#O(maxLength)
            if manifest[n]["DeliveryDeadline"] == "EOD":
                manifestEODList.append(manifest[n])
            else:
                newManifest.append(manifest[n])
        manifest = newManifest

        #This organizes exception packages by earliest time
        if len(manifest) > 0: 
            manifest = order_by_least_time(manifest)# O(maxLength**3)
            manifest = sort_by_distance(manifest)# O(maxLength**3 + 2p)

        #adding least Distance Nodes to manifest
        manifest = manifest + sortedEarliestTimePackages
        manifest = cut_time(manifest, hubAddress)
        #adding group EOD Packages
        manifest = manifest + manifestEODList
        if Table.count_delayed_packages(beginningTime) > 0:#needs to be timely packages to be delivered O(h)
                manifest = sort_by_distance(manifest)# O(maxLength**3 + 2p)
                return manifest
        else:
            #sorting EOD Packages by distance from eachother
            sortedEODPackages = sort_by_distance(eodPackages)# O(e**3 + 2p)
            for index in range(0, len(sortedEODPackages)):
                if len(manifest) < maxLoad:
                    package = sortedEODPackages[index]

                    #handling wrong address packages
                    if package["Exceptions"] != None:
                        if package["Exceptions"][0] == "WrongAddress":
                            # if the time the wrong address package is updated 
                            # is not less than or equal to the input beginningTime 
                            # then continue
                            if package["Exceptions"][2] > beginningTime:
                                continue
                        #Comparing arrival times of delayed packages against beginningTime
                        elif package["Exceptions"][0] == "Delayed":
                            if convert_time(package["Exceptions"][1]) > beginningTime:
                                continue
                    #adding EOD Packages to manifest
                    manifest.append(package)
                else:
                    break
    #no more timely packages to deliver
    else:
        if len(eodPackages) != 0:
            #sorting EOD Packages by distance from eachother
            sortedEODPackages = sort_by_distance(eodPackages)# O(e**3 + 2p) e= #of eod packages in hash Table
            for index in range(0, len(sortedEODPackages)):
                if len(manifest) < maxLoad:
                    package = sortedEODPackages[index]
                    #handling wrong address packages
                    if package["Exceptions"]  != None:
                        if package["Exceptions"][0] == "WrongAddress":
                            # if the time the wrong address package is updated 
                            # is not less than or equal to the input beginningTime 
                            # then continue
                            if package["Exceptions"][2] > beginningTime:
                                continue
                        #Comparing arrival times of delayed packages against beginningTime
                        elif package["Exceptions"][0] == "Delayed":
                            if convert_time(package["Exceptions"][1]) > beginningTime:
                                continue
                    #adding EOD Packages to manifest
                    manifest.append(package)
                else:
                    break
    #try:
    if manifest != []:
        #reorderying manifest by distance, furthur reducing travel time and distance to travel
        manifest = sort_by_distance(manifest)# O(maxLength**3 + 2p)
    return manifest
 
def get_delivery_status(truck1, truck2):

    """ This is a menu function used to display truck statistics 
    to the user. Runs in linear time O(n) where n is the # of 
    elements within table """
   
    truck1Manifest = truck1.get_manifest()
    truck2Manifest = truck2.get_manifest()
    print("====================Truck1====================")
    print("Trucker Name: ", truck1.get_trucker_name())
    print("Time of Last Drop Off: ", convert_time_to_string(truck1.get_last_drop_off_time()))
    print("Truck1 Total Distance: ", truck1.get_total_distance())
    print("------------------->Manifest")
    if truck1Manifest == []:
        print("No Packages Loaded")
    else:
        print_package_list(truck1Manifest)

    input("Press enter to continue: ")
    print("====================Truck2====================")
    print("Trucker Name: ", truck2.get_trucker_name())
    print("Time of Last Drop Off: ", convert_time_to_string(truck2.get_last_drop_off_time()))
    print("Truck2 Total Distance: ", truck2.get_total_distance())
    print("------------------->Manifest")
    if truck2Manifest == []:
        print("No Packages Loaded")
    else:
        print_package_list(truck2Manifest)

def ui(truck1, truck2, table):
    """ This handles the user interface allowing the user to interact 
    with the program. Runs in linear time O(n) where n is the # of 
    elements within table"""

    print("""
    get delivery status of each truck: 1
    retrieve all packages: 2
    Lookup a Package: 3
    Add a Package: 4
    Continue: 5
    """)
    userInput = input("Select an option from above: ")

    #checking the user input for errors
    try:
        userInput = int(userInput)
    #the user entered in a string or didn't enter in anything
    except:
        print("------------------------->ERROR: INVALID INPUT<-------------------------")
        input("Press enter to continue: ")
        return 0

    #displaying truck delivery status
    if userInput == 1:
        get_delivery_status(truck1, truck2)
        input("Press enter to continue: ")
        return 0

    #displaying the contents of the hash table
    elif userInput == 2:
        table.print_hash()
        input("Press enter to continue: ")
        return 0

    #Menu for looking up packages from the hash table
    elif userInput == 3:
        #requesting parameter information to lookup the package
        print("Enter in information without spaces!")
        idInput = str(input("Enter in ID#: "))
        addressInput = str(input("Enter in street address: "))
        deliveryDeadlineInput = input("Enter in the delivery deadline: ")
        cityInput = input("Enter in delivery city: ")
        weightInput = str(input("Enter in package Weight: "))

        print("""Status Type
        1: En Rout To Carrier Facility
        2: At Local Carrier Facility
        3: En Rout
        4: Delivered""")
        statusInput = input("Select a package status: ")
        try:
            statusSelection = int(statusInput)
    
        #user entered in non integer character(s)
        except:
            print("------------------------->ERROR: INVALID INPUT<-------------------------")
            input("Press enter to continue: ")
        if statusSelection == 1:
            statusInput = "En Rout To Carrier Facility"
        elif statusSelection == 2:
            statusInput = "At Local Carrier Facility"
        elif statusSelection == 3:
            statusInput = "En Rout"
        elif statusSelection == 4:
            statusInput = "Delivered"
        #user input > 4
        else:
            print("Select an option from the list above: ")
            return 0
        #retrieving the package from table
        package = table.get_package_using_params(idInput, addressInput, deliveryDeadlineInput, cityInput, weightInput, statusInput)
        #success case, the package is found
        if package != 0:
            print("----PACKAGE FOUND----")
            print_package_list([package])
        #failure case the package was not found
        else:
            print("The Specified Package Doesnot Exists!")
        input("Press enter to continue: ")
        return 0

    #create packages and store them in the hash table
    elif userInput == 4:
        print("===============Package=Creator===============")
        print("Enter in information without spaces!")
        idInput = input("Enter in ID#: ")
        addressInput = input("Enter in street address: ")
        deliveryDeadlineInput = input("Enter in the delivery deadline: ")
        cityInput = input("Enter in delivery city: ")
        weightInput = input("Enter in package Weight: ")
        print()
        print("""Status Type
        1: En Rout To Carrier Facility
        2: At Local Carrier Facility
        3: En Rout
        4: Delivered""")
        statusInput = "At Local Carrier Facility"#default value
        statusSelection = input("Enter in package Status: ")
        if statusSelection == 1:
            statusInput = "En Rout To Carrier Facility"
        elif statusSelection == 2:
            statusInput = "At Local Carrier Facility"
        elif statusSelection == 3:
            statusInput = "En Rout"
        elif statusSelection == 4:
            statusInput = "Delivered"
        else:
            print("Select an option from the list above: ")
        addStatus = table.add_package_with_params(idInput, addressInput, cityInput, deliveryDeadlineInput, weightInput, statusInput)        
        if addStatus == 0:
            print("Error: Failed to Add Package")
        elif addStatus == 2:
            print("Error: Package ID already assigned")
        else:
            print("----PACKAGE CREATED----")
            #displaying to the user the package stored in the hash table
            print_package_list([table.get_package_using_id(idInput)])
        input("Press enter to continue: ")
        return 0

    #case the user exits the ui and continues the program
    elif userInput == 5:
        newTime = input("Enter in a time: ")
        return (1, newTime) 

    #case the user enters in an integer greater than 5
    else:
        print("------------------------->ERROR: INVALID INPUT<-------------------------")
        input("Press enter to continue: ")
        return 0

def limited_ui(truck1, truck2, Table):
    """ This handles a limited version of the user interface this is 
    used towards the end of the program once all packages have been
    delivered. Runs in linear time O(n) where n is the # of 
    elements within table"""

    print("""
    get delivery status of each truck: 1
    retrieve all packages: 2
    Lookup a Package: 3
    Exit: 4""")
    userInput = input("Select an option from above: ")

    #checking the user input for errors
    try:
        userInput = int(userInput)
    #the user entered in a string or didn't enter in anything
    except:
        print("------------------------->ERROR: INVALID INPUT<-------------------------")
        input("Press enter to continue: ")
        return 0

    #displaying truck delivery status
    if userInput == 1:
        get_delivery_status(truck1, truck2)
        input("Press enter to continue: ")
        return 0

    #displaying the contents of the hash table
    elif userInput == 2:
        table.print_hash()
        input("Press enter to continue: ")
        return 0

    #Menu for looking up packages from the hash table
    elif userInput == 3:
        #requesting parameter information to lookup the package
        print("Enter in information without spaces!")
        idInput = str(input("Enter in ID#: "))
        addressInput = str(input("Enter in street address: "))
        deliveryDeadlineInput = input("Enter in the delivery deadline: ")
        cityInput = input("Enter in delivery city: ")
        weightInput = str(input("Enter in package Weight: "))

        print("""Status Type
        1: En Rout To Carrier Facility
        2: At Local Carrier Facility
        3: En Rout
        4: Delivered""")
        statusInput = input("Select a package status: ")
        try:
            statusSelection = int(statusInput)
    
        #user entered in non integer character(s)
        except:
            print("------------------------->ERROR: INVALID INPUT<-------------------------")
            input("Press enter to continue: ")
        if statusSelection == 1:
            statusInput = "En Rout To Carrier Facility"
        elif statusSelection == 2:
            statusInput = "At Local Carrier Facility"
        elif statusSelection == 3:
            statusInput = "En Rout"
        elif statusSelection == 4:
            statusInput = "Delivered"
        #user input > 4
        else:
            print("Select an option from the list above: ")
            return 0
        #retrieving the package from table
        package = table.get_package_using_params(idInput, addressInput, deliveryDeadlineInput, cityInput, weightInput, statusInput)
        #success case, the package is found
        if package != 0:
            print("----PACKAGE FOUND----")
            print_package_list([package])
        #failure case the package was not found
        else:
            print("The Specified Package Doesnot Exists!")
        input("Press enter to continue: ")
        return 0
    #exit case
    elif userInput == 4:
        return 1

    #case the user enters in an integer greater than 5
    else:
        print("------------------------->ERROR: INVALID INPUT<-------------------------")
        input("Press enter to continue: ")
        return 0

def main():

    """ This function is where the core algorithm is implemented not
    created. Reading the two files provided in the folder with the 
    python files the function creates a list of Node addresses, and a  
    list of Package objects. Package objects are inserted into the hash. 
    Two delivery trucks are created, their manifests are initialized 
    using the core algorithm generate_manifest. Function compeltes once 
    all packages  have been marked as Delivered. This function runs in 
    polynomial time O(t**3 + b**3 + e**3) where t is the number of truck 
    specific packages b is the number of timely packages and e is the
    number of eod packages."""
    #parsing file data and generating package and node objects
    x = File('WGUPS Distance Table.csv', 'WGUPS Package File.csv')
    nodeData = x.extract_distance_data() #O(p**2) p = # of delivery points
    #        hubInfo = [Title, City, State, Zip, BeginningCounter, Address]
    hubAddress = nodeData[1][5]
    packageList = x.extract_package_data(240, nodeData[0])
    #adding package objects to hash table
    Table = HashTable(packageList[0])
    for n in range(1, len(packageList)):# range (1, PackageListLength) because Package at index 0 is used to initialize the hash table O(ic) i = elements in packageList c=# of characters in zip and address
        Table.add_sort(packageList[n])
    
    #Gathering Exception Data
    delayedPackages = Table.gather_delayed_packages()# O(h) = # of pakages in the hash table

    #generating Truck objects
    truck1 = Truck("Jamie", [], hubAddress)
    truck2 = Truck("Rick", [], hubAddress)

    
    #tracks time entered in by the user
    userTime = 0
    print("--------------------->Truck Delivery Simulator<---------------------")

    #calling user interface before program begins
    #calling the user interface
    status = 0#stores the exit case for ui
    while status == 0:
        #when status is 0 the user entered invalid input
        #when status is 1 the user exited the ui and continue the program
        status = ui(truck1, truck2, Table)
    #how much long the simulation should run
    userTime = convert_time(status[1])

    #Initializing Manifest for the first time

    #truck1:
    truck1.set_manifest(generate_manifest(Table, "1", hubAddress, 16, 8))# O(t**3 + b**3 + e**3) t = #of truck specific packages, b = # of timely packages, e = # of eod packages
    Table.update_hash_delivery_status(truck1.get_manifest(), "En Rout") 
    truck1Case = 0

    #truck2:
    truck2.set_manifest(generate_manifest(Table, "2", hubAddress, 16, 8))# O(t**3 + b**3 + e**3)
    Table.update_hash_delivery_status(truck2.get_manifest(), "En Rout")# O(nch) n = manifest length, c = address length + zip length, h = number of elements in the hash table
    truck2Case = 0
 
    truck2TotalManfifest = truck2.get_manifest()
    #tracks a simulation time for the program
    globalTime=8.0#24 hour format

    #Delivery System
    while True:

        if globalTime <= userTime:
            #squeezing out the last few minutes before global reaches 
            #the specified userTime to more accuratly portray deliveries
            #and status updates
            if globalTime + .5 > userTime:
                globalTime = userTime

            #updating DeliveryAddress for Package 9
            if globalTime >= 10.5:
                Table.update_package_address("410SStateSt", "At Local Carrier Facility", "9", globalTime)# O(h)
        
            #updataing any delayed Packages that have arrived at the carrier facility
            #O(h**2)
            if delayedPackages != []:
                for index in range(0, len(delayedPackages)):# O(dch) d = # of delayed packages
                    delayedPackage = delayedPackages[index]
                    if delayedPackage["Status"] == "En Rout To Carrier Facility":
                        #Checking arrival time agains globalTime
                        if (convert_time(delayedPackage["Exceptions"][1]) < globalTime):
                            #updating the Package status within the hash table
                            Table.update_package_status(delayedPackage, "At Local Carrier Facility")# O(ch)
            #truck1

            #since each truck has an independant internal clock this allows
            #the internal clock to catch up with the global time the 
            #limitation is that truck1 may return to the hub later than
            #truck2 but truck1 is loaded before truck2 since it is the
            #first while loop

            while True:# O(t**3 + b**3 + e**3) h=#number of pckgs in the hash

                #the internal clock of truck1 is compared against globalTime
                if truck1.get_time_of_next_drop_off() <= globalTime:
                    # manifest is empty sending truck1 to the Hub to reload
                    if truck1.get_manifest() == []:
                        #truck1's current location is set to the hubAddress
                        truck1.set_current_local(hubAddress)
                        print("Truck 1 has returned to the Carrier Facility")
                        #loading truck1's manifeset using generate_manifest
                        truck1.set_manifest(generate_manifest(Table, "1", hubAddress, 16, truck1.get_time_of_next_drop_off()))# O(t**3 + b**3 + e**3)
                        #updating the newly loaded packages in the hashTable
                        Table.update_hash_delivery_status(truck1.get_manifest(), "En Rout")# O(nch)

                        #this is the case when there are no packages left to load into truck1
                        if truck1.get_manifest() == []:
                            truck1Case = 1
                            break

                        continue
                    elif truck1Case == 1:
                        break

                    #delivering packages
                    else:
                        #deliveruing a package
                        newPackage = truck1.get_next_package_drop_off()
                        #recording the time the package was delivered
                        timeOfDelivery = convert_time_to_string(truck1.get_last_drop_off_time())
                        #updating the hash table
                        Table.update_package_status(newPackage, "Delivered", timeOfDelivery)# O(ch)
                        #displaying the package delivered to the user
                        print("Package: ", newPackage["ID"], " Delivered", " : ", (timeOfDelivery), " Truck1")
                        print()#spacer
                        #setting a new destination to the hub to load more packages
                        if truck1.get_manifest() == []:
                            #calculating time to reach the hub
                            time = float(truck1.get_last_delivered_package().lookup_distance(hubAddress)[1]) / 18 + truck1.timeOfNextDropOff# O(p)
                            truck1.set_time_of_next_drop_off(time)
                            continue
                else:
                    break
        
            #truck2
            #this handles the while loop for truck2
            while True:
                #accounting for delayed packages
                #truck 2 collects the delayed packages once the next 
                #Package to deliver is an EOD deadline.
                if len(truck2.get_manifest()) != 0:
                    if truck2.get_manifest()[0]["DeliveryDeadline"] == "EOD":
                        #checking if new packages have been added or arrived
                        #checking if the packages are EOD or timely
                        if Table.count_delayed_packages(truck2.get_internal_time()) > 0:
                            #setting next destination to carrier facility for reload
                            #calculating the time that truck will take to arrive at the hub
                            time = float(truck2.get_last_delivered_package().lookup_distance(hubAddress)[1]) / 18 + truck2.timeOfNextDropOff 
                            #setting the time as the next drop off time
                            truck2.set_time_of_next_drop_off(time)
                            if truck2.get_time_of_next_drop_off() <= globalTime:
                                truck2.set_current_local(hubAddress)
                                #displaying to the user that truck 2 is at the hub
                                print("Truck 2 has returned to the Carrier Facility")
                                newManifest = generate_manifest(Table, "2", hubAddress, 16-len(truck2.get_manifest()), truck2.get_time_of_next_drop_off())
                                truck2.set_manifest(newManifest + truck2.get_manifest())
                                Table.update_hash_delivery_status(truck2.get_manifest(), "En Rout")
                                continue

                if truck2.get_time_of_next_drop_off() <= globalTime:
                    #sending truck1 to the Hub to reload
                    if truck2.get_manifest() == [] and truck2Case != 1:
                        #setting the current location as the hub
                        truck2.set_current_local(hubAddress)
                        #displaying the time truck2 arrived at the hub
                        print("Truck 2 has returned to the Carrier Facility: ", convert_time_to_string(truck2.get_last_drop_off_time()))
                        #loading packages into manifest
                        truck2.set_manifest(generate_manifest(Table, "2", hubAddress, 16, truck2.get_time_of_next_drop_off()))
                        #updating Packages inside hashTable to "En Rout"
                        Table.update_hash_delivery_status(truck2.get_manifest(), "En Rout")

                        #This is the case that there are no more packages to deliver for truck2
                        if truck2.get_manifest() == []:
                            truck2Case = 1
                            break
                        else:
                            continue

                    elif truck2Case == 1:
                        break
               
                    #delivery
                    else:
                        #Deliver package
                        newPackage = truck2.get_next_package_drop_off()
                        #recording the time of delivery
                        timeOfDelivery = convert_time_to_string(truck2.get_last_drop_off_time())
                        #displaying the delivered package to the user
                        Table.update_package_status(newPackage, "Delivered", timeOfDelivery)
                        #updating the Package instance in HashTable
                        print("Package: ", newPackage["ID"], " Delivered", " : ", timeOfDelivery, " Truck2")
                        print()#spacer
                        #setting a new destination
                        if truck2.get_manifest() == []:
                            #returning to Hub
                            #calculating the time until arrival at the hub
                            time = float(truck2.get_last_delivered_package().lookup_distance(hubAddress)[1]) / 18 + truck2.timeOfNextDropOff
                            #setting that time as the next drop off time
                            truck2.set_time_of_next_drop_off(time)
                            continue
                else:
                    break

        #determining if the all packages have been delivered
        if Table.get_packages_not_delivered() == 0:
            print("===============All=Packages=Delivered===============")
            print("Total Distance: ", round(truck1.get_total_distance() + truck2.get_total_distance()), " Miles")#rounding the total distance       
            #calling the user interface
            status = 0#stores the exit case for ui
            while status == 0:
                #when status is 0 the user entered invalid input
                #when status is 1 the user exited the ui and continue the program
                status = limited_ui(truck1, truck2, Table)
            break

        #incrementing global time by 30 minutes
        #this makes it so the user sees a broad update rather than 
        #minute by minute update
        if globalTime + .5 < userTime:
            globalTime += .5

        elif globalTime + .1 < userTime:
            globalTime += .1

        elif globalTime + .01 < userTime:
            globalTime += .01
        
        ##breaking once internal timer is equel to user's timer
        #if globalTime == userTime:
        #    break

        
        if globalTime == userTime:
            #calling the user interface
            status = 0#stores the exit case for ui
            #This loop executed until the user enters in a valid time
            while True:
                while status == 0:
                    #when status is 0 the user entered invalid input
                    #when status is 1 the user exited the ui and continue the program
                    status = ui(truck1, truck2, Table)
                #how much long the simulation should run
                userTime = convert_time(status[1])
                #invalid time entered since the entered time is less than the globalTime
                if userTime < globalTime:
                    print("Incorrect Time Please enter in a valid Time")
                else:
                    break

    #Displaying all Packages inside the HashTable to the user
    print("===============All=Packages=Delivered===============")
    Table.print_hash()

    print("===============All=Packages=Delivered===============")

    print("Total Distance: ", round(truck1.get_total_distance() + truck2.get_total_distance()), " Miles") #rounding the total distance
main()                  