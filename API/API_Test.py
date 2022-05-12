#######################################################
# Author : RedNeath                                   #
# Licensed under MIT (head to /LICENSE for more info) #
#                                                     #
# Copyright © 2022 Kamigami no Tanjou                 #
#######################################################

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

def main():
    #test_servers()
    #test_users()
    test_reaction_roles()
    test_commands()
    test_characters()
    test_stats()
    test_warnings()

def test_servers():
    #POST request for a server :
    print("POST request for a server :")
    response = post(API + "servers", json={"ID" : 933640317121474610})
    print(response.json())

    print()
    input("Go to : " + API + "server/933640317121474610 to see the changes, then press enter.")
    print()

    #PUT request for a server :
    print("PUT request for a server :")
    response = put(API + "server/933640317121474610", json={"mutedUsers" : 280341659789819904, "mutedRole" : 772749593573457971, "maxWarn" : 5, "cooldown" : 155, "banned" : 444444444444444444, "warnings" : 0, "prefix" : "dif", "autoRoles" : 444444444444444444, "reactionRoles" : 0, "customCommands" : 0})
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

def test_users():
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

def test_reaction_roles():
    #POST request for a reaction role :
    print("POST request for a reaction role :")
    response = post(API + "reaction_roles", json={"message" : 950721904409456640, "role" : 772749555384844299, "emote" : ""})
    print(response.json())

    print()
    input("Go to : " + API + "reaction_role/1 to see the changes, then press enter.")
    print()

    #PUT request for a reaction role :
    print("PUT request for a reaction role :")
    response = put(API + "reaction_role/1", json={"message" : 950721882141896745, "role" : 928643883636764693, "emote" : "test"})
    print(response.json())

    print()
    input("Go to : " + API + "reaction_role/1 to see the changes, then press enter.")
    print()

    #GET request for a reaction role :
    print("GET request for a reaction role :")
    response = get(API + "reaction_role/0")
    print(response.json())

    print()
    input("Press Enter to continue...")
    print()

    #DELETE request for a reaction role :
    print("DELETE request for a user :")
    response = delete(API + "reaction_role/1")
    print(response.json())

    print()
    input("Go to : " + API + "reaction_roles to see the changes, then press enter.")
    print()

def test_commands():
    #POST request for a command :
    print("POST request for a command :")
    response = post(API + "commands", json={"name" : "It's a mee!", "output" : "Marioo!"})
    print(response.json())

    print()
    input("Go to : " + API + "command/1 to see the changes, then press enter.")
    print()

    #PUT request for a command :
    print("PUT request for a command :")
    response = put(API + "command/1", json={"name" : "Oh... Actually,", "output" : "I'm just a stone lover :man_shrugging:"})
    print(response.json())

    print()
    input("Go to : " + API + "command/1 to see the changes, then press enter.")
    print()

    #GET request for a command :
    print("GET request for a command :")
    response = get(API + "command/0")
    print(response.json())

    print()
    input("Press Enter to continue...")
    print()

    #DELETE request for a command :
    print("DELETE request for a command :")
    response = delete(API + "command/1")
    print(response.json())

    print()
    input("Go to : " + API + "commands to see the changes, then press enter.")
    print()

def test_characters():
    #POST request for a character :
    print("POST request for a character :")
    response = post(API + "characters", json={"firstname" : "Flygara", "lastname" : "Harri", "genre" : "Femme", "specie" : "Humaine", "class" : "Prêtresse de l'Harmonie", "alignment" : "Loyal Bon", "beliefs" : "Flyjungfrisme", "stats" : [0, 1, 2, 3, 4, 5], "equipment" : "None", "spells" : "Magie des plumes\nMagie de soins", "image" : "https://media.discordapp.net/attachments/887775828497293372/956267285755080805/Flygara_head_only_sans_signature.png"})
    print(response.json())

    print()
    input("Go to : " + API + "character/1 to see the changes, then press enter.")
    print()

    #PUT request for a character :
    print("PUT request for a character :")
    response = put(API + "character/1", json={"firstname" : "Yulian", "lastname" : "Mikov", "genre" : "Homme", "specie" : "Humaine", "class" : "Commandant de Vartak", "alignment" : "Neutre Bon", "beliefs" : "Flyjungfrisme", "stats" : [6, 7, 8, 9, 10, 11], "equipment" : "None", "spells" : "Magie de pression", "image" : "https://media.discordapp.net/attachments/887775828497293372/947140133193383997/Yulian_Mikov_head_only_unsigned.png"})
    print(response.json())

    print()
    input("Go to : " + API + "character/1 to see the changes, then press enter.")
    print()

    #GET request for a character :
    print("GET request for a reaction role :")
    response = get(API + "character/0")
    print(response.json())

    print()
    input("Press Enter to continue...")
    print()

    #DELETE request for a user :
    print("DELETE request for a character :")
    response = delete(API + "character/1")
    print(response.json())

    print()
    input("Go to : " + API + "characters to see the changes, then press enter.")
    print()

def test_stats():
    #POST request for a stat :
    print("POST request for a stat :")
    response = post(API + "stats", json={"name" : "test", "value" : 0})
    print(response.json())

    print()
    input("Go to : " + API + "stat/6 to see the changes, then press enter.")
    print()

    #PUT request for a stat :
    print("PUT request for a stat :")
    response = put(API + "stat/6", json={"name" : "not a test anymore", "value" : 999999999999999999})
    print(response.json())

    print()
    input("Go to : " + API + "stat/6 to see the changes, then press enter.")
    print()

    #GET request for a stat :
    print("GET request for a stat :")
    response = get(API + "stat/0")
    print(response.json())

    print()
    input("Press Enter to continue...")
    print()

    #DELETE request for a stat :
    print("DELETE request for a stat :")
    response = delete(API + "stat/6")
    print(response.json())

    print()
    input("Go to : " + API + "stats to see the changes, then press enter.")
    print()

def test_warnings():
    #POST request for a warning :
    print("POST request for a warning :")
    response = post(API + "warnings", json={"user" : 437934657737195522})
    print(response.json())

    print()
    input("Go to : " + API + "warning/1 to see the changes, then press enter.")
    print()

    #GET request for a warning :
    print("GET request for a warning :")
    response = get(API + "warning/0")
    print(response.json())

    print()
    input("Press Enter to continue...")
    print()

    #DELETE request for a user :
    print("DELETE request for a user :")
    response = delete(API + "warning/1")
    print(response.json())

    print()
    input("Go to : " + API + "warnings to see the changes, then press enter.")
    print()

main()