# nokia-xml-tools


## GSM, UMTS

### [compareXML_TXT](compareXML_TXT.py)
Compare actual ADxx network XML exports [^1] to neighbour creation plan [^2]. This script will output 3 text files: tokeep, tocreate, todelete.
 
### [deleteADJG](deleteADJG.py)
Create XML script from neighbour deletion plan [^2]. This is done by parsing network XML export [^1].

### [replaceADJS](replaceADJS.py)
Update and define replacement ADJS to new destination cells. This script will generate XML script with updated neighbours by parsing network XML export [^1].

### [ADJXparser](ADJXparser.py)
Create JSON files with ADJS and ADJG usage per cell. This is done by parsing network XML export [^1]. This is a CLI app, show CLI help with '-h'.

### [externalUMTSAdjs](externalUMTSAdjs.py)
Uses JSON output from [ADJXparser](ADJXparser.py) to create ADJS neighbour creation XML script for external UMTS cells with neighbour addition file [^3]. This is a CLI app, show CLI help with '-h'.


## LTE

### [cellTracing](cellTracing.py)
Add cell tracing capabilities by providing list of MRBTS IDs [^4]. This script will generate XML script by parsing network XML export [^2].


[^1]: The following steps should be followed to generate bulk CM exports:
	1. As the omc user, log in to a virtual machine where the scripting service is running.
	2. Execute the following command: `[omc]$ racclimx.sh -op Import_Export -fileFormat RAML2 -importExportOperation actualExport -fileName myFileName.xml -UIValues true`.
[^2]: Neighbour .txt plans must be provided in the format `Create/Delete, SOURCE CELL ID, DESTINATION CELL ID`.
[^3]: ADJS neighbour .csv addition file must be provided in the format `SCI,DCI,MCC,MNC,LAC,RAC,SC,RNC`, where SCI - ID of source cell and DCI - ID, MCC - mobile country code, MNC-  mobile network code, LAC - location area code, RAC - routing area code, SC - scrambling code of destination cell.
[^4]: MRBTS ID assumed with format XXYYY, with X being the area ID and Y being the site ID.