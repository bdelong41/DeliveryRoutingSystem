from PackageClass import Package
from NodeClass import Node
import copy
class File(object):
    def __init__(self, distanceFileName, packageFileName):#O(1)
        """ File names are entered in here along with there extension and used to 
            open the necessary files. Files are opened in read only mode.
            The idea of reading the file data is to read the data 
            without changing it assuming the files structure remains 
            constant in every scenario that involves the use of this program"""
        self.distanceFileData = ""
        self.distanceLength = 0
        self.packageData = ""
        self.packageLength = 0

        with open(distanceFileName, 'r') as file:
            self.distanceFileData = file.read()
            self.distanceLength = len(self.distanceFileData)
        file.close()

        with open(packageFileName, 'r') as file:
            self.packageData = file.read()
            self.packageLength = len(self.packageData)
        file.close()

    def extract_node_info(self):# O(c) where c is the number of characters in the first half of the document
        """ Here WGUPS Distance Table.csv is being traversed. each 
        chunck delimeted by a comma is converted into raw node 
        information refered to as the variable "nodeSentence" which is 
        then appended to node list. Each nodeSentence is pieced together
        each itteration, charactors such as quotations and commas as 
        well as spaces are ignored. Starting from index 284 the file 
        data is read until a string of two commas is detected indicating 
        the start of the second set consisting of the distance stastics
        The function then returns a tuple containing nodeList, index for 
        reference of the second set of information."""
        nodeSentence = ""
        nodeList = [] 
        indexCounter = 0

        #using 284 as a jumping point to get past preliminary data
        for index in range(284, self.distanceLength): # O(c) where c is the number of characters in the first half of the document
            if self.distanceFileData[index] == "\"":#Excluding Quotations
                if self.distanceFileData[index + 1] == "," or self.distanceFileData[index - 1] == ",":#indicates the start of the second row
                    continue
                else:
                    nodeList.append(nodeSentence)#adding the final node to nodeList
                    return (nodeList, index, len(nodeList))

            #storing nodesentence into nodelist
            elif self.distanceFileData[index] == ",":
                nodeList.append(nodeSentence)
                nodeSentence = ""

            #adding data to nodesentence
            else:
                nodeSentence = nodeSentence + self.distanceFileData[index]

#    def __init__(self, DeliveryAddress, ZipCode, DeliveryState):
    def sepparate_address_from_zip(self,address_Zip):
        """ This sepparates a string input "address_Zip" and looks for
        an opening parenthisis which will delimit address and zip.
        The resulting information is then returned as a tuple (address, zip)
        1060 Dalton Ave S (84104).
        Address: 1060 Dalton Ave S 
        Delimiter: (
        Zip: 84104
        Closing Delimiter: )
        """
        stage = 0
        address = ""
        zip = ""
        #Sepparting ZipInfo
        nodeList = []
        for counter in range(0, len(address_Zip)):# O(c) c = # of chars in the address_zip variable
            if stage == 1:
                if address_Zip[counter] == ")":
                    return (address, zip)
                else:
                    zip = zip + address_Zip[counter]
            elif address_Zip[counter] == "(":
                stage = 1
            else:
                address = address + address_Zip[counter]

    def get_hub_info(self, StartingIndex):

        """ get_hub_info extracts raw text string given "startingIndex" 
        and sorts it into title, city, state, zip, address, and distance
        statistics providing a starting point for delivery. Distances are
        calculated by referencing the address extracted here. As in the 
        previous functions "commaCounter" is used to track the number of 
        comma delimiters, this tells the function which determines which 
        field if being filled out. 
        First comma: title info 
        Second comma: state and zip which is broken down by "sepparate_address_from_zip "
        Third comma: Extranious info "hub" 
        Fourth comma: Distance statistics.
        """

        commaCounter = 0
        title = "" #consists of name and address
        sentence = ""
        city = ""
        state = ""
        zip = ""
        address = ""
        distance = ""
        finishingIndex = 0

        for index in range(StartingIndex, self.distanceLength):
            if self.distanceFileData[index] == "\"":
                continue

            elif self.distanceFileData[index] == ",":
                if commaCounter == 0:#storing sentence in title
                    title = sentence
                    sentence = ""
                    commaCounter = commaCounter + 1
                elif commaCounter == 1:#storing sentence in city
                    city = sentence
                    sentence = ""
                    commaCounter += 1
                elif commaCounter == 2:#storing sentence into zip and state
                    #stripping sentence down into ascii integer and non-ascii integer chars
                    for counter in range(0, len(sentence)):
                        #sepparating state info from zip "UT 84107"
                        if ord(sentence[counter]) >= 48 and ord(sentence[counter]) <= 57:#cheking if the character is an integer in ascii
                            zip = zip + sentence[counter]#adding integer data to zip sentence
                        else:
                            state = state + sentence[counter]#if the char is not an integer then add to state sentence
                    sentence = ""
                    commaCounter += 1
                elif commaCounter == 3:#resetting sentence to empty string
                    sentence = ""
                    commaCounter += 1
                elif commaCounter == 4:#adding sentence to distance stats, there is only one point 0.0
                    distance = sentence
                    sentence = ""
                    commaCounter += 1
                    finishingIndex = index
            #adding to sentence one character per itteration
            else:
                sentence = sentence + self.distanceFileData[index]
        #traverssing through comma line delimeters
        for counter in range(finishingIndex, self.distanceLength):
            if self.distanceFileData[counter] == ",":
                continue
            else:
                #extracting a starting destination to break other nodes down
                beginningCounter = counter#locates the start of the next section
                break
        sentence = ""

        #sepparating address from title
        for index2 in range(0, len(title)):
            if ord(title[index2]) >= 47 and ord(title[index2]) <= 58:
                address = title[index2:]
                break

        #returning the following data points as a tuple
        return (title, city, state, zip, beginningCounter, address)

    def extract_distance_info(self, startingIndex):
        """ extract_distance sorts the text data into four attributes
            title, address, zip, and distanceData.
            The number of concurrent delimeters scanned indicates the 
            position in the line. The variable sentence adds  
            characters together one itteration at a time creating one 
            string of data. The program ignores extranious data such  
            as spaces, commas and quotations when adding characters to 
            the sentence variable. Once a delimiter is found "sentence"  
            is then added to one of four attributes using comma stage.
            These are the four comma stages:
            stage 0: title data "International Peace Gardens 1060 Dalton Ave S"
            stage 1: address and zip information "1060 Dalton Ave S (84104)"
                here both data points are sepparated and stored sepparatly
            stage 2: distance information "7.2,0.0"
            stage 3: line break
            """

        #should remove
        sentence = ""
        title = ""# consists of name and address
        address =  "" 
        zip = ""


        distances = []
        node_distance_data = [title, address, zip, distances]
        nodeInfo = [] #Stores Node_distance_data
        commaStage = 0 #stage 0 means title stage: 1 address and zip stage: 2 distance data stage: 3 means line break
        nodeList = []

        for index in range(startingIndex, self.distanceLength):#starting from startingIndex

            #this handles line breaks
            if commaStage == 3:#indicates string of comma delimiters meaning a line break
                if self.distanceFileData[index] == "\"":
                    #Issues with referencing use deepcopy to ensure data is copied
                    nodeInfo.append(copy.deepcopy(node_distance_data))
                    node_distance_data[0] = ""
                    node_distance_data[1] = ""
                    node_distance_data[2] = ""
                    node_distance_data[3] = []
                    commaStage = 0
                else:
                    continue

            elif index == self.distanceLength - 1:
                nodeInfo.append(copy.deepcopy(node_distance_data))#adding final part of the distance information
                #This adds the missing 0.0 for the last node
                nodeInfo[len(nodeInfo) - 1][len(nodeInfo[len(nodeInfo) - 1]) - 1].append("0.0")
                finalStage = index
                return nodeInfo

            #eliminating quotes
            elif self.distanceFileData[index] == "\"":#skips quotes
                continue

            #singular comma delimiter indicates different field
            elif self.distanceFileData[index] == ",":
                #storing title data
                if commaStage <= 2:
                    if commaStage == 0:
                        node_distance_data[0] = str.strip(sentence).replace(" ","")                      
                        commaStage += 1
                    elif commaStage == 1:
                        #sepparating address and zip info
                        node_distance_data[1] = str.strip(self.sepparate_address_from_zip(sentence)[0]).replace(" ","")
                        node_distance_data[2] = str.strip(self.sepparate_address_from_zip(sentence)[1]).replace(" ","")
                        commaStage += 1
                    elif commaStage == 2:
                        #print("2: ",str.strip(sentence))
                        node_distance_data[3].append(str.strip(sentence).replace(" ", ""))
                sentence = ""#reseting sentence
                if self.distanceFileData[index: (index + 2)] == ",,":#linebreak
                    commaStage = 3
                elif self.distanceFileData[index - 4: index] == ",0.0":#final linebreak of the file
                    commaStage = 3

            else:
                sentence = sentence + str.strip(self.distanceFileData[index]).replace(" ", "")

    def extract_package_data(self, startingIndex, nodeList):
        """ extract_package_data sifts "packageData" for package data 
            elements. by tracking the number of consecutive delimiters
            this function determines it's position in the row. The 
            number of commas encounter in a row is recorded in 
            commaCounter. There are a maximum of twelve commas per 
            line, when all twelve have been found the function moves to
            the new line. The First comma indicates package ID, second 
            comma delivery address, third comma city namefourth comma  
            state information, fith comma  delivery deadline, sixth 
            comma weight, seventh comma special notes.for readabilty 
            "attributeList" stores variables labeled after each 
            attribute.
            """
        #attributes
        packageList = []
        sentence = ""# Sentence accepts any charactor other than ","
        packageID = ""
        address = ""
        city = ""
        state = ""
        zip = ""
        deliveryDeadline = ""
        mass = ""
        specialNotes = ""   
        attributeList = [packageID, address, city, state, zip, deliveryDeadline, mass, specialNotes]
        attributeDescription = ["PackageID", "Address", "City", "State", "Zip", "Deadline", "Mass", "SpecialNotes"]
        #AttributeCounter tracks whether attriubutes have been filled; 0: packageID, 7: SpecialNotes
        attributeCounter = 0
        #CommaCounter of value less than 7 means attributes are still being explored
        commaCounter = 0
        #QuoteCounter tracks opening and closing quotes to temporarily disable Comma tracking
        quoteCounter = 0
        sentence = ""


        for traversalIndex in range(startingIndex, self.packageLength):
            if self.packageData[traversalIndex] == "," and quoteCounter == 0:
                commaCounter += 1 # this will track the number of commas is less than or equal to 7
                if commaCounter <= 8:
                    attributeList[attributeCounter] = sentence
                    #str.strip() prevents \n from appearing as a result of concatination
                    #Incrementing AttributeCounter
                    attributeCounter += 1
                    sentence = ""
                elif commaCounter > 7 and commaCounter < 12:#Traversal is exploring ending line commas there are 5 ending commas
                    continue
                elif commaCounter == 12:# Traversal is finished exploring ending line commas and a new line starts next itteration
                    packageObject = Package(attributeList[0], attributeList[1], attributeList[2], attributeList[3], attributeList[4], attributeList[5], attributeList[6], attributeList[7], nodeList)# O(p) p = # of delivery points
                    packageList.append(packageObject)
                    attributeCounter = 0
                    commaCounter = 0
                    continue

            elif self.packageData[traversalIndex] == "\"":
                quoteCounter += 1
                sentence = sentence + self.packageData[traversalIndex]
                if quoteCounter == 2:
                    quoteCounter = 0

            elif self.packageData[traversalIndex] == " ":
                continue

            else:
                sentence = sentence + self.packageData[traversalIndex]
        return packageList 

    def extract_distance_data(self):

        """ Combines extract_node_info() get_hub_info() and 
        extract_distance_info to create node objects. This function 
        only gathers data from the distance table. The distance Table is 
        divided into two halves. extract_node_info provides a starting 
        index for get_hub_info. get_hub_info provides necassary
        information for the hub our starting point for all deliveries 
        as well as a beginning index for extract_distance_info. 
        DistanceInfo contains n number of lists used to initialize 
        Node objects. once a Node object is created the 
        distanceRange data member is initialized using addressRange.
        addressRange is made of a tuple (address, distance) where 
        address is the address of another Node and distance is the
        physical distance to that node. Distance data shown in the 
        table is only half filled out, this missing data is extrapolated
        using the third for loop in this function."""
        nodeList = []
        nodeInfo = self.extract_node_info()
        hubInfo = self.get_hub_info(nodeInfo[1])#entering starting index from nodeInfo

        distanceInfo = self.extract_distance_info(hubInfo[4])#using starting index provided from hubinfo
        distanceInfo.insert(0, [hubInfo[0], hubInfo[5], hubInfo[3], ["0.0"]])

        for index in range(0, len(distanceInfo)):# O(p**2) p = # of delivery nodes
            node_distance_data = distanceInfo[index]
            #Node newNode(address, zip, city)
            newNode = Node(node_distance_data[1], node_distance_data[2], hubInfo[2])
            #fusing Node Info with distance data
            #distance data will be a subset of each node

            #addressRange is gathered both horizontally and vertically 

            #Here distance is known but the address is determined by
            #exploring from beginning node data to the current node data being used
            for counter in range(0, index + 1):# O(k) k = # of nodes above the current node in the file matrix
                addressRange = (distanceInfo[counter][1], distanceInfo[index][3][counter])
                newNode.add_distance_range(addressRange)

            #Extracting distances from nodes below the current node
            #by using an x,y coordinate, where x is the row number 
            #of the current node and y is the address of the relating node 
            for counter2 in range(index + 1, len(distanceInfo)):# O(i) i = # of nodex below the current node in teh file maxtrix i + k = total # number of delivery nodes p
                #addressRange = (y,x); y=Address; x=distance
                addressRange = (distanceInfo[counter2][1], distanceInfo[counter2][3][index])
                newNode.add_distance_range(addressRange)
            #adding newNode to nodeList
            nodeList.append(newNode)

        return (nodeList, hubInfo)

        

