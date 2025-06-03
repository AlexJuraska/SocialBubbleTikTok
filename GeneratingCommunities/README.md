This directory contains scripts to create communities from the data from Data gathering.

First file [fileGetter.py](fileGetter.py).

DATA_SOURCE - .json file, passed into DataParser as first parameter dataFile

LEIDEN_DATA_SOURCE - .json file, into which Leiden communities will be placed

LOUVAIN_DATA_SOURCE - .json file, into which Louvain communities will be placed

Next use [leidenCommunityGeneration.py](leidenCommunityGeneration.py) to create Leiden communities or [louvainCommunityGeneration.py](louvainCommunityGeneration.py) for Louvain.

File [RelationshipExtractor.py](RelationshipExtractor.py) doesn't need to be used.