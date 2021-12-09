import xml.etree.ElementTree as ET
import re

def ADJS_toClear(XMLroot, sourceCells):
    distNames = {}
    neighbours = []
    for cellID in sourceCells: ## loop dictionary keys
        counter = 0
        print('_' * 10)
        for i in range(0, sourceCells[cellID]): ## loop dictionary value (ADJS to clear) 
            for cmData in XMLroot:
                for managedObject in cmData:
                    if (managedObject.attrib.get('class') == 'ADJS' and (("/WCEL-"+ str(cellID)) in managedObject.attrib.get('distName')) ):
                        for data in managedObject:
                            if (data.attrib.get('name') == 'AdjsCI'):
                                if (not ((str(cellID) + ',' + str(data.text)) in neighbours) and (counter < sourceCells[cellID])):
                                    neighbours.append(str(cellID) + ',' + str(data.text))
                                    counter += 1   
                                    print (managedObject.attrib.get('distName'))
                                    #print (ET.dump(managedObject))
                                    distNames.update(({(managedObject.attrib.get('distName')): cellID})) # adding the element
        print(str(counter) + ' neighbours found for ' + str(cellID))
    return distNames    

filename1 = input("Enter XML filename: ") + '.xml' ## File from NetACT exports
XMLroot = ET.parse(filename1).getroot()
generatedXML = '<?xml version="1.0"?><raml xmlns="raml21.xsd" version="2.1"><cmData type="plan" scope="all" name="replace_ADJS">'

# creating an empty dictionary
sourceCells = {}
 
# number of elements as input
n = int(input("Enter number of unique cells to clear: "))
 
# iterating till the range
for i in range(0, n):
    key = int(input("Enter source cell ID: "))
    val = int(input("Enter number of ADJS to clear: "))
    sourceCells.update(({key: val})) # adding the element

print('_' * 10)  
dest_RNCID = int(input("Enter destination RNC: "))
dest_MCC = int(input("Enter destination MCC: "))
dest_MNC = int(input("Enter destination MNC: "))
dest_LAC = int(input("Enter destination LAC: "))
dest_RAC = int(input("Enter destination RAC: "))

for distName, cellId in ADJS_toClear(XMLroot, sourceCells).items():
    print('_' * 10)
    print('Define destination for ' + distName)
    dest_ID = int(input("Enter destination ID: "))
    dest_scrCode = int(input("Enter destination SCR Code: "))
    
    generatedXML += '<managedObject class="ADJS" version="RNC20FP4" distName="' + distName + '" operation="update">'
    generatedXML += '<p name="AdjsMCC">' + str(dest_MCC) + '</p>'
    generatedXML += '<p name="AdjsMNC">' + str(dest_MNC) + '</p>'
    generatedXML += '<p name="AdjsRNCid">' + str(dest_RNCID) + '</p>'
    generatedXML += '<p name="AdjsCI">' + str(dest_ID) + '</p>'
    generatedXML += '<p name="AdjsLAC">' + str(dest_LAC) + '</p>'
    generatedXML += '<p name="AdjsRAC">' + str(dest_RAC) + '</p>'
    generatedXML += '<p name="AdjsScrCode">' + str(dest_scrCode) + '</p>'
    generatedXML += '<p name="ADJSChangeOrigin">NetAct RNW plan originated configuration action</p><p name="AdjsCPICHTxPwr">33.0</p><p name="AdjsDERR">No</p><p name="AdjsEcNoOffset">0.0</p><p name="AdjsSIB">For SIB and CELL DCH meas</p><p name="AdjsTxDiv">Tx Diversity not used</p><p name="AdjsTxPwrRACH">24</p><p name="HSDPAHopsIdentifier">13</p><p name="NrtHopsIdentifier">12</p><p name="RTWithHSDPAHopsIdentifier">14</p><p name="RtHopsIdentifier">11</p><p name="SRBHopsIdentifier">Not defined</p>'
    generatedXML += '</managedObject>'

generatedXML += '</cmData></raml>'
        
with open("output.xml", "w") as f:
    f.write(generatedXML)