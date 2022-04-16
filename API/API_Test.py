#The goal of ths python script is to test the insertion of data
#in the API via POST and/or PUT requests 

from requests import post
from requests import put #Not used yet
from sys import argv

#The address of the API (can be entered as a parameter when
#launching the script in the terminal).
#Note that the URL provided should end with a '/'!!
API = "http://127.0.0.1:5000/"
if len(argv) > 1 :
    API = argv[1]

#POST request for a server :
response = post(API + "servers", {"ID" : 933640317121474610})
print(response)