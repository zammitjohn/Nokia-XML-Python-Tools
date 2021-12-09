import xml.etree.ElementTree as ET
import re

def ADJG_toClear(XMLroot, line):
    line = line.strip().replace('Create,', '').replace('Delete,', '')
    sourceCellID = re.search(r".*?(?=,)", line).group(0)
    destinationCellID = re.search(r"(?<=,).*", line).group(0)

    for cmData in XMLroot:
        for managedObject in cmData:
            if (managedObject.attrib.get('class') == 'ADJG' and (("/WCEL-"+ str(sourceCellID)) in managedObject.attrib.get('distName')) ):
                for data in managedObject:
                    if (data.attrib.get('name') == 'AdjgCI'):
                        if (str(data.text) == destinationCellID):
                            return managedObject.attrib.get('distName') # match!


filename1 = input("Enter XML filename: ") + '.xml' ## File from NetACT exports
filename2 = input("Enter TXT filename: ") + '.txt' ## File from planning
XMLroot = ET.parse(filename1).getroot()
txtLines = open(filename2, 'r')
neigh_parsed_txt = []
generatedXML = '<?xml version="1.0"?><raml xmlns="raml21.xsd" version="2.1"><cmData type="plan" scope="all" name="delete_ADJG">'

for line in txtLines:
    distName = ADJG_toClear(XMLroot, line)
    if (distName):
        generatedXML += '<managedObject class="ADJG" version="RNC20FP4" operation="delete" distName="' + distName + '"/>'

generatedXML += '</cmData></raml>'        
with open("output.xml", "w") as f:
    f.write(generatedXML)