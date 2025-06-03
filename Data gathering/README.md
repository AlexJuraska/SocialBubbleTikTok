This directory contains the files needed for getting and processing data from the social media platform TikTok.

First to generate the files, you have 2 options

1. Tampermonkey 
   1. Set it up
   2. Paste the code from [tampermonkeyScript.js](tampermonkeyScript.js) into a new userscript
2. DOM
   1. Open DOM -> Console
   2. Paste the [tampermonkeyScript.js](tampermonkeyScript.js) into the console

Then when you have the files, you can move on to [jsonTransfer.py](jsonTransfer.py).

With this you first need to create an instance of class DataParser, into which you will pass 2 .json files - one for the data and the other for hashtag data.

Then the functionality is separated into 2 parts
1. Comments
   1. parseFileCommentsData() where you need to pass the path to a single file with the comments
   2. parseDirectoryCommentsData() which is the same thing but you pass a whole directory
2. Follows
   1. parseFileCommentsData() where you need to pass the path to a single file with the comments
   2. parseDirectoryCommentsData() which is the same thing but you pass a whole directory

All of these will store the information into the .json files specified at the start.