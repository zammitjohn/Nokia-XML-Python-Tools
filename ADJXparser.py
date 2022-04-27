"""
ADJXparser.py
Create JSON files with ADJS and ADJG usage per cell. This is done by parsing network XML export.
"""

import sys
import getopt
import xml.etree.ElementTree as ET
import json
import re
from mergedeep import merge

def print_usage():
    print ('ADJXparser.py -i <XML input file> -o <JSON output file>')

def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        (opts, args) = getopt.getopt(argv, 'hi:o:', ['ifile=', 'ofile='])
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)
    for (opt, arg) in opts:
        if opt == '-h':
            print_usage()
            sys.exit()
        elif opt in ('-i', '--ifile'):
            inputfile = arg
        elif opt in ('-o', '--ofile'):
            outputfile = arg

    if inputfile == '' or outputfile == '':
        print ('Required parameters missing. See ADJXparser.py -h')
        sys.exit(2)

    XMLroot = ET.parse(inputfile).getroot()
    adjsData = {}
    adjgData = {}

    print("Parsing..")
    for cmData in XMLroot:
        for managedObject in cmData:
                if (managedObject.attrib.get('class') == 'ADJS'): ## 3G to 3G
                     rncId = (str(re.search(r"(?<=/RNC-).*?(?=/WBTS-)", str(managedObject.attrib)).group(0)))
                     wbtsId = (str(re.search(r"(?<=/WBTS-).*?(?=/WCEL-)", str(managedObject.attrib)).group(0)))
                     cellId = (str(re.search(r"(?<=/WCEL-).*?(?=/ADJS-)", str(managedObject.attrib)).group(0)))
                     adjsId = (re.search(r"(?<=/ADJS-).*?(?=')", str(managedObject.attrib)).group(0))
                     if (cellId in adjsData):   
                         adjsData[cellId]['idUsedADJS'].append(adjsId)
                         adjsData[cellId]['qtyUsedADJS'] += 1
                     else:
                        adjsData[cellId] = {'rncId': rncId, 'wbtsId': wbtsId, 'qtyUsedADJS': 1, 'idUsedADJS': [adjsId]} 
                elif (managedObject.attrib.get('class') == 'ADJG'): ## 3G to 2G
                     rncId = (str(re.search(r"(?<=/RNC-).*?(?=/WBTS-)", str(managedObject.attrib)).group(0)))
                     wbtsId = (str(re.search(r"(?<=/WBTS-).*?(?=/WCEL-)", str(managedObject.attrib)).group(0)))
                     cellId = (str(re.search(r"(?<=/WCEL-).*?(?=/ADJG-)", str(managedObject.attrib)).group(0)))
                     adjgId = (re.search(r"(?<=/ADJG-).*?(?=')", str(managedObject.attrib)).group(0))
                     if (cellId in adjgData):   
                         adjgData[cellId]['idUsedADJG'].append(adjgId)
                         adjgData[cellId]['qtyUsedADJG'] += 1
                     else:
                        adjgData[cellId] = {'rncId': rncId, 'wbtsId': wbtsId, 'qtyUsedADJG': 1, 'idUsedADJG': [adjgId]}                             
                
    merged = merge(adjsData, adjgData)

    with open(outputfile, 'w') as fp:
        json.dump(merged, fp)

    print("Output")
    print(merged)

if __name__ == '__main__':
    main(sys.argv[1:])