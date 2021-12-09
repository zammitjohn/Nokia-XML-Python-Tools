import xml.etree.ElementTree as ET
import re

def neighbour_parser(XMLroot):
    neighbours = []
    for cmData in XMLroot:
        for managedObject in cmData:
            if (managedObject.attrib.get('class') == 'ADCE'): ## 2G to 2G 
                for data in managedObject:
                    if (data.attrib.get('name') == 'adjacentCellIdCI'):
                        bcfid = ('%03d' % int(re.search(r"(?<=/BCF-).*?(?=/BTS-)", str(managedObject.attrib)).group(0)))
                        btsid = int(re.search(r"(?<=/BTS-).*?(?=/ADCE-)", str(managedObject.attrib)).group(0))
                        sectorId = (btsid - round(btsid/10)*10 + 1)
                        sourceCell = int(str(sectorId) + '0' + str(bcfid))
                        destinationCell = int(data.text)
                        neighbours.append(str(sourceCell) + ',' + str(destinationCell))
       
            if (managedObject.attrib.get('class') == 'ADJW'): ## 2G to 3G
                for data in managedObject:
                    if (data.attrib.get('name') == 'AdjwCId'):
                        bcfid = ('%03d' % int(re.search(r"(?<=/BCF-).*?(?=/BTS-)", str(managedObject.attrib)).group(0)))
                        btsid = int(re.search(r"(?<=/BTS-).*?(?=/ADJW-)", str(managedObject.attrib)).group(0))
                        sectorId = (btsid - round(btsid/10)*10 + 1)
                        sourceCell = int(str(sectorId) + '0' + str(bcfid))
                        destinationCell = int(data.text)
                        neighbours.append(str(sourceCell) + ',' + str(destinationCell))        

            if (managedObject.attrib.get('class') == 'ADJS'): ## 3G to 3G (intra-frequency)
                for data in managedObject:
                    if (data.attrib.get('name') == 'AdjsCI'):
                        sourceCell = int(re.search(r"(?<=/WCEL-).*?(?=/ADJS-)", str(managedObject.attrib)).group(0))
                        destinationCell = int(data.text)
                        neighbours.append(str(sourceCell) + ',' + str(destinationCell))              

            if (managedObject.attrib.get('class') == 'ADJG'): ## 3G to 2G
                for data in managedObject:
                    if (data.attrib.get('name') == 'AdjgCI'):
                        sourceCell = int(re.search(r"(?<=/WCEL-).*?(?=/ADJG-)", str(managedObject.attrib)).group(0))
                        destinationCell = int(data.text)
                        neighbours.append(str(sourceCell) + ',' + str(destinationCell))

            if (managedObject.attrib.get('class') == 'ADJI'): ## 3G to 3G (inter-frequency)
                for data in managedObject:
                    if (data.attrib.get('name') == 'AdjiCI'):
                        sourceCell = int(re.search(r"(?<=/WCEL-).*?(?=/ADJI-)", str(managedObject.attrib)).group(0))
                        destinationCell = int(data.text)
                        neighbours.append(str(sourceCell) + ',' + str(destinationCell))                     
    
    return neighbours

filename1 = input("Enter XML filename: ") + '.xml' ## File from NetACT exports
filename2 = input("Enter TXT filename: ") + '.txt' ## File from planning
XMLroot = ET.parse(filename1).getroot()
txtLines = open(filename2, 'r')
neigh_parsed_txt = []

neigh_parsed_xml = neighbour_parser(XMLroot)
print(neigh_parsed_xml)
print('_' * 10)
print ('Done, parsed ' + str(len(neigh_parsed_xml)) + ' managedObjects from XML')
print('_' * 10)

for line in txtLines:
    neigh_parsed_txt.append(line.strip().replace('Create,', '').replace('Delete,', ''))
neigh_parsed_txt = list(set(neigh_parsed_txt)) # remove potential duplicates
print(neigh_parsed_txt)
print('_' * 10)
print ('Done, parsed ' + str(len(neigh_parsed_txt)) + ' lines from TXT')
print('_' * 10)


# Neighbours to delete
f = open("todelete.txt", "w")
for i in neigh_parsed_xml:
    if (i not in neigh_parsed_txt):
        f.write('Delete,' + i + '\n')
  
# Neighbours to create
f = open("tocreate.txt", "w")
for i in neigh_parsed_txt:
    if (i not in neigh_parsed_xml):
        f.write('Create,' + i + '\n')
   
# Neighbours to remain unchanged
f = open("tokeep.txt", "w")
for i in neigh_parsed_xml:
    if (i in neigh_parsed_txt):
        f.write(i + '\n')