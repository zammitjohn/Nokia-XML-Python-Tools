import xml.etree.ElementTree as ET
import json
import re

XMLroot = ET.parse("export.xml").getroot()
cellData = {}

### 3G
## loop WCELs
print("Loading WCEL")
for cmData in XMLroot:
    for managedObject in cmData:
        if (managedObject.attrib.get('class') == 'WCEL'):
            for data in managedObject:
                if (data.attrib.get('name') == 'CId'):
                    cellData[data.text] = {'qtyUsedADJS': 0, 'idUsedADJS': []}  


## loop ADJS
print("Loading ADJS")
for key in cellData:
    adjsCount = 0
    for cmData in XMLroot:
        for managedObject in cmData:
                if (managedObject.attrib.get('class') == 'ADJS'): ## 3G to 3G (intra-frequency)
                     if ((str(re.search(r"(?<=/WCEL-).*?(?=/ADJS-)", str(managedObject.attrib)).group(0))) == key):
                         adjsCount += 1
                         adjsId = (re.search(r"(?<=/ADJS-).*?(?=')", str(managedObject.attrib)).group(0))
                         cellData[key]['qtyUsedADJS'] = adjsCount
                         cellData[key]['idUsedADJS'].append(adjsId)
                   

with open('result.json', 'w') as fp:
    json.dump(cellData, fp)
    
print(cellData)                   
                