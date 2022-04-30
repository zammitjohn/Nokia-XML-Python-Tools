"""
externalUMTSAdjs.py
Create neighbour creation XML script for external UMTS cells with neighbour addition file. 
"""

import sys
import getopt
import csv
import json

def print_usage():
    print ('externalUMTSAdjs.py -i <JSON neighbour input file> -n <CSV neighbour addition file> -o <XML output file>')

def main(argv):
    inputfile_1 = ''
    inputfile_2 = ''
    outputfile = ''
    try:
        (opts, args) = getopt.getopt(argv, 'hi:n:o:', ['ifile=', 'nfile=', 'ofile='])
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)
    for (opt, arg) in opts:
        if opt == '-h':
            print_usage()
            sys.exit()
        elif opt in ('-i', '--ifile'):
            inputfile_1 = arg
        elif opt in ('-n', '--nfile'):
            inputfile_2 = arg			
        elif opt in ('-o', '--ofile'):
            outputfile = arg		

    if inputfile_1 == '' or inputfile_2 == '' or outputfile == '':
        print ('Required parameters missing. See externalUMTSAdjs.py -h')
        sys.exit(2)

	## Import neighbours JSON file
    with open(inputfile_1, 'r') as JSON:
        json_dict = json.load(JSON)
		
    generatedXML = '<?xml version="1.0"?><raml xmlns="raml21.xsd" version="2.1"><cmData type="plan" scope="all">'
    
	## Loop neighbours CSV file
    with open(inputfile_2, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['SCI'] in json_dict:
                if (json_dict[row['SCI']]['qtyUsedADJS'] < 31):
                    print('Generating ADJS for', row['SCI'])
                    for avail_adjsID in range(1, 32):
                        if str(avail_adjsID) in json_dict[row['SCI']]['idUsedADJS']: # find next available ADJS ID
                            continue
                        else:
                            generatedXML += '<managedObject class="ADJS" distName="PLMN-PLMN/RNC-' + json_dict[row['SCI']]['rncId'] + '/WBTS-' + json_dict[row['SCI']]['wbtsId'] + '/WCEL-' + row['SCI'] + '/ADJS-' + str(avail_adjsID) + '">'
                            generatedXML += '<p name="AdjsMCC">' + row['MCC'] + '</p>'
                            generatedXML += '<p name="AdjsMNC">' + row['MNC'] + '</p>'
                            generatedXML += '<p name="AdjsRNCid">' + json_dict[row['SCI']]['rncId'] + '</p>'
                            generatedXML += '<p name="AdjsCI">' + row['DCI'] + '</p>'
                            generatedXML += '<p name="AdjsLAC">' + row['LAC'] + '</p>'
                            generatedXML += '<p name="AdjsRAC">' + row['RAC'] + '</p>'
                            generatedXML += '<p name="AdjsScrCode">' + row['SC'] + '</p>'
                            generatedXML += '<p name="AdjsRNCid">' + row['RNC'] + '</p>'
                            generatedXML += '<p name="ADJSChangeOrigin">NetAct RNW plan originated configuration action</p><p name="AdjsCPICHTxPwr">33.0</p><p name="AdjsDERR">No</p><p name="AdjsEcNoOffset">0.0</p><p name="AdjsSIB">For SIB and CELL DCH meas</p><p name="AdjsTxDiv">Tx Diversity not used</p><p name="AdjsTxPwrRACH">24</p><p name="HSDPAHopsIdentifier">3</p><p name="NrtHopsIdentifier">2</p><p name="RTWithHSDPAHopsIdentifier">4</p><p name="RtHopsIdentifier">1</p><p name="SRBHopsIdentifier">Not defined</p>'
                            generatedXML += '</managedObject>'
                            break
						  
                else:
                    print('No free ADJS for', row['SCI'])
            else:
                print(row['SCI'], 'does not exist!')
                
        generatedXML += '</cmData></raml>'
    
    with open(outputfile, "w") as f:
        f.write(generatedXML)

if __name__ == '__main__':
    main(sys.argv[1:])