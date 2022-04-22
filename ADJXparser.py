import xml.etree.ElementTree as ET
import json
import re
from mergedeep import merge

XMLroot = ET.parse("export.xml").getroot()
adjsData = {}
adjgData = {}

## loop ADJS
print("Loading ADJS")
for cmData in XMLroot:
    for managedObject in cmData:
            if (managedObject.attrib.get('class') == 'ADJS'): ## 3G to 3G
                 cellId = (str(re.search(r"(?<=/WCEL-).*?(?=/ADJS-)", str(managedObject.attrib)).group(0)))
                 adjsId = (re.search(r"(?<=/ADJS-).*?(?=')", str(managedObject.attrib)).group(0))
                 if (cellId in adjsData):   
                     adjsData[cellId]['idUsedADJS'].append(adjsId)
                     adjsData[cellId]['qtyUsedADJS'] += 1
                 else:
                    adjsData[cellId] = {'qtyUsedADJS': 1, 'idUsedADJS': [adjsId]} 


## loop ADJG
print("Loading ADJG")
for cmData in XMLroot:
    for managedObject in cmData:
            if (managedObject.attrib.get('class') == 'ADJG'): ## 3G to 2G
                 cellId = (str(re.search(r"(?<=/WCEL-).*?(?=/ADJG-)", str(managedObject.attrib)).group(0)))
                 adjgId = (re.search(r"(?<=/ADJG-).*?(?=')", str(managedObject.attrib)).group(0))
                 if (cellId in adjgData):   
                     adjgData[cellId]['idUsedADJG'].append(adjgId)
                     adjgData[cellId]['qtyUsedADJG'] += 1
                 else:
                    adjgData[cellId] = {'qtyUsedADJG': 1, 'idUsedADJG': [adjgId]}                     

merged = merge(adjsData, adjgData)

with open('result.json', 'w') as fp:
    json.dump(merged, fp)
    
print(merged)