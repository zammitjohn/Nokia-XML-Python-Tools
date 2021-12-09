# Nokia-XML-Tools

## [compareXML_TXT](compareXML_TXT.py)
Compare actual ADxx network XML exports to neighbour creation plan [^1]. This script will output 3 text files: tokeep, tocreate, todelete.
 
## [deleteADJG](deleteADJG.py)
Create XML script from neighbour deletion plan [^1]. This is done by parsing an network XML export.

## [replaceADJS](replaceADJS.py)
Update and define replacement ADJS to new destination cells. This script will generate XML script with updated neighbours by parsing network XML export. 

[^1]: Neighbour .txt plans must be provided in the format `Create/Delete, *SOURCE CELL ID*, *DESTINATION CELL ID*`.