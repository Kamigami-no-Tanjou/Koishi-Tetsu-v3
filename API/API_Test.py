#The goal of ths python script is to test the insertion of data
#in the API via POST, PUT, GET and DELETE requests 

from requests import post
from requests import put
from requests import get
from requests import delete
from sys import argv

#The address of the API (can be entered as a parameter when
#launching the script in the terminal).
#Note that the URL provided should end with a '/'!!
API = "http://127.0.0.1:5000/"
if len(argv) > 1 :
    API = argv[1]

#POST request for a server :
print("POST request for a server :")
response = post(API + "servers", json={"ID" : 933640317121474610})
print(response.json())

print()
input("Go to : " + API + "server/933640317121474610 to see the changes, then press enter.")
print()

#PUT request for a server :
print("PUT request for a server :")
response = put(API + "server/933640317121474610", json={"mutedUsers" : 280341659789819904, "mutedRole" : 772749593573457971, "maxWarn" : 5, "cooldown" : 155, "banned" : 444444444444444444, "prefix" : "dif", "autoRoles" : 444444444444444444, "reactionRoles" : 0, "customCommands" : 0})
print(response.json())

print()
input("Go to : " + API + "server/933640317121474610 to see the changes, then press enter.")
print()

#GET request for a server :
print("GET request for a server :")
response = get(API + "server/772740999058817026")
print(response.json())

print()
input("Press Enter to continue...")
print()

#DELETE request for a server :
print("DELETE request for a server :")
response = delete(API + "server/933640317121474610")
print(response.json())

print()
input("Go to : " + API + "server/933640317121474610 to see the changes, then press enter.")
print()

#POST request for a user :
print("POST request for a user :")
response = post(API + "users", json={"ID" : 523804235217895430})
print(response.json())

print()
input("Go to : " + API + "user/523804235217895430 to see the changes, then press enter.")
print()

#PUT request for a user :
print("PUT request for a user :")
response = put(API + "user/523804235217895430", json={"servers" : 772740999058817026, "characters" : 0, "exp" : 200, "birthdate" : "01/01"})
print(response.json())

print()
input("Go to : " + API + "user/523804235217895430 to see the changes, then press enter.")
print()

#GET request for a user :
print("GET request for a user :")
response = get(API + "user/280341659789819904")
print(response.json())

print()
input("Press Enter to continue...")
print()

#DELETE request for a user :
print("DELETE request for a user :")
response = delete(API + "user/523804235217895430")
print(response.json())

print()
input("Go to : " + API + "user/523804235217895430 to see the changes, then press enter.")
print()