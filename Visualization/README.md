This directory contains scripts to create the visualization.

First Cytoscape needs to be downloaded:
https://cytoscape.org/

Next to add the nodes and edges to the program, you need to create CSV files to upload to it.

[jsonToCSV.py](Cytoscape/jsonToCSV.py) will create a CSV file with the edges

[communitiesToCSV.py](Cytoscape/communitiesToCSV.py) will create a CSV with separate colors for the communities

[edgesAddendumToCSV.py](Cytoscape/edgesAddendumToCSV.py) will create a CSV which will add the users themselves as separate columns, not just as edges

[ideologySelectionToCSV.py](Cytoscape/ideologySelectionToCSV.py) will add colors based on selected ideology (liberal, conservative, news)

In all of these, .json files need to be added where the info will be gathered from, as well as .csv files for output

DATA_FILE - .json file with the data from Data Gathering
COMM_FILE - .json file with the wanted community data
OUTPUT_FILE - .csv output file 