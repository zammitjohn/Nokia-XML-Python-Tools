# nokia-xml-tools

## GSM, UMTS

### [compareXML_TXT](compareXML_TXT.py)
Compare actual ADxx network XML exports [^1] to neighbour creation plan [^2]. This script will output 3 text files: tokeep, tocreate, todelete.
 
### [deleteADJG](deleteADJG.py)
Create XML script from neighbour deletion plan [^2]. This is done by parsing network XML export [^1].

### [replaceADJS](replaceADJS.py)
Update and define replacement ADJS to new destination cells. This script will generate XML script with updated neighbours by parsing network XML export [^1].

### [ADJXparser](ADJXparser.py)
Create JSON files with ADJS and ADJG usage per cell. This is done by parsing network XML export [^1].

## LTE

### [cellTracing](cellTracing.py)
Add cell tracing capabilities by providing list of MRBTS IDs [^3]. This script will generate XML script by parsing network XML export [^2].

[^1]: The following steps should be followed to generate bulk CM exports:
	1. As the omc user, log in to a virtual machine where the scripting service is running.
	2. Execute the following command: `[omc]$ racclimx.sh -op Import_Export -fileFormat RAML2 -importExportOperation actualExport -fileName myFileName.xml -UIValues true`.
[^2]: Neighbour .txt plans must be provided in the format `Create/Delete, SOURCE CELL ID, DESTINATION CELL ID`.
[^3]: MRBTS ID assumed with format XX-YYY, with X being the area ID and Y being the site ID.