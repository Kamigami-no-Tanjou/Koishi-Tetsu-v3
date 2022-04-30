from xml.dom.pulldom import CHARACTERS
from numpy import char
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
from flask_cors import CORS
import json

app = Flask(__name__)
api = Api(app)
cors = CORS(app)

#CONSTANTS :
#-----------

#Paths of the json files
SERVERS = "./DATA/SERVERS.json"
USERS = "./DATA/USERS.json"
REACTION_ROLES = "./DATA/REACTIONROLES.json"
COMMANDS = "./DATA/COMMANDS.json"
CHARACTERS = "./DATA/CHARACTERS.json"
STATS = "./DATA/STATS.json"


#-----------------------------------------------------------------------------------------
# We start by defining the request parsers for the different requests that needs one.
# A request parser allows us to define the different attributes that we want in a request.
#-----------------------------------------------------------------------------------------

#request parser for a POST request on the server list :
serv_post_args = reqparse.RequestParser()
serv_post_args.add_argument("ID", type=int, required=True)
serv_post_args.add_argument("users", type = int, default=[], action='append')
serv_post_args.add_argument("maxWarn", type=int, default=3)
serv_post_args.add_argument("cooldown", type=int, default=150)
serv_post_args.add_argument("banned", type=int, default=[], action='append')
serv_post_args.add_argument("prefix", type=str, default='kt')
serv_post_args.add_argument("autoRoles", type=int, default=[], action='append')
serv_post_args.add_argument("reactionRoles", type=int, default=[], action='append')
serv_post_args.add_argument("customCommands", type=int, default=[], action='append')

#request paresr for a PUT request on the server list :
serv_put_args = reqparse.RequestParser()
serv_put_args.add_argument("users", type=int, action='append')
serv_put_args.add_argument("maxWarn", type=int)
serv_put_args.add_argument("cooldown", type=int)
serv_put_args.add_argument("banned", type=int, action='append')
serv_put_args.add_argument("prefix", type=str)
serv_put_args.add_argument("autoRoles", type=int, action='append')
serv_put_args.add_argument("reactionRoles", type=int, action='append')
serv_put_args.add_argument("customCommands", type=int, action='append')

#We create a list of servers and add the content of the ./DATA/SERVERS.json to it.
with open(SERVERS, "r") as rf:
	servers = json.load(rf) 

#request parser for a POST request on the user list :
user_post_args = reqparse.RequestParser()
user_post_args.add_argument("ID", type=int, required=True)
user_post_args.add_argument("characters", action='append')
user_post_args.add_argument("muted", type=int)
user_post_args.add_argument("warnings", type=int)
user_post_args.add_argument("exp", type=int)
user_post_args.add_argument("birthdate", type=str)

#request parser for a PUT request on the user list :
user_put_args = reqparse.RequestParser()
user_put_args.add_argument("characters", action='append')
user_put_args.add_argument("muted", type=int)
user_put_args.add_argument("warnings", type=int)
user_put_args.add_argument("exp", type=int)
user_put_args.add_argument("birthdate", type=str)

#We create a list of users and add the content of the ./DATA/USERS.json to it.
with open(USERS, "r") as rf:
	users = json.load(rf)

#request parser for a POST request on the reaction role list :
reacrole_post_args = reqparse.RequestParser()
reacrole_post_args.add_argument("ID", type=int, required=True)
reacrole_post_args.add_argument("channel", type=int, required=True)
reacrole_post_args.add_argument("role", type=int, required=True)
reacrole_post_args.add_argument("emote", type=str, required=True)

#request parser for a PUT request on the reaction role list :
reacrole_put_args = reqparse.RequestParser()
reacrole_put_args.add_argument("ID", type=int)
reacrole_put_args.add_argument("channel", type=int)
reacrole_put_args.add_argument("role", type=int)
reacrole_put_args.add_argument("emote", type=str)

#We create a list of reaction roles and add the content of the ./DATA/REACTIONROLES.json to it.
with open(REACTION_ROLES, "r") as rf:
	reaction_roles = json.load(rf)

#request parser for a POST request on the command list :
commands_post_args = reqparse.RequestParser()
commands_post_args.add_argument("ID", type=int, required=True)
commands_post_args.add_argument("name", type=str, required=True)

#request parser for a PUT request on the command list :
commands_put_args = reqparse.RequestParser()
commands_put_args.add_argument("ID", type=int)
commands_put_args.add_argument("name", type=str)

#We create a list of commands and add the content of the ./DATA/COMMANDS.json to it.
with open(COMMANDS, "r") as rf:
	commands = json.load(rf)

#request parser for a POST request on the character list :
char_post_args = reqparse.RequestParser()
char_post_args.add_argument("ID", type=int, required=True)
char_post_args.add_argument("firstname", type=str)
char_post_args.add_argument("lastname", type=str)
char_post_args.add_argument("genre", type=str)
char_post_args.add_argument("specie", type=str)
char_post_args.add_argument("class", type=str)
char_post_args.add_argument("alignment", type=str)
char_post_args.add_argument("beliefs", type=str)
char_post_args.add_argument("stats", action='append')
char_post_args.add_argument("equipment", type=str)
char_post_args.add_argument("spells", type=str)
char_post_args.add_argument("image", type=str)

#request parser for a PUT request on the character list :
char_put_args = reqparse.RequestParser()
char_put_args.add_argument("ID", type=int)
char_put_args.add_argument("firstname", type=str)
char_put_args.add_argument("lastname", type=str)
char_put_args.add_argument("genre", type=str)
char_put_args.add_argument("specie", type=str)
char_put_args.add_argument("class", type=str)
char_put_args.add_argument("alignment", type=str)
char_put_args.add_argument("beliefs", type=str)
char_put_args.add_argument("stats", action='append')
char_put_args.add_argument("equipment", type=str)
char_put_args.add_argument("spells", type=str)
char_put_args.add_argument("image", type=str)

#We create a list of characters and add the content of the ./DATA/CHARACTERS.json to it.
with open(CHARACTERS, "r") as rf:
	characters = json.load(rf)

#request parser for a POST request on the stats list :
stats_post_args = reqparse.RequestParser()
stats_post_args.add_argument("ID", type=int, required=True)
stats_post_args.add_argument("name", type=str, required=True)
stats_post_args.add_argument("value", type=int, required=True)

#request parser for a PUT request on the stats list :
stats_put_args = reqparse.RequestParser()
stats_put_args.add_argument("ID", type=int)
stats_put_args.add_argument("name", type=str)
stats_put_args.add_argument("value", type=int)

#We create a list of stats and add the content of the ./DATA/STATS.json to it.
with open(STATS, "r") as rf:
	stats = json.load(rf)

#-------------------------------
# Existence verification methods
#-------------------------------

#Aborts the extraction of a server's data if the server's ID isn't in the list.
def abort_if_server_id_doesnt_exist(server_id):
	for i in range(len(servers)):
		if server_id == servers[i]["ID"]:
			#In that case the ID is found here, so there's no need to go and search for it any longer.
			#Still we return the index, so we don't have to search the whole list once again.
			return i
	
	abort(404, message="Invalid server ID")
			

#Aborts the insertion of a server's data if the server's ID already exists.
def abort_if_server_id_already_exists(server_id):
	for i in range(len(servers)):
		if server_id == servers[i]["ID"]:
			abort(409, message="Server already in the list")

#Aborts the extraction of a user's data if the user's ID isn't in the list.
def abort_if_user_id_doesnt_exist(user_id):
	for i in range(len(users)):
		if user_id == users[i]["ID"]:
			return #In that case the ID is found here, so there's no need to go and search for it any longer
	
	abort(404, message="Invalid user ID")

#Aborts the insertion of a user's data if the user's ID already exists.
def abort_if_user_id_already_exists(user_id):
	for i in range(len(users)):
		if user_id == users[i]["ID"]:
			abort(409, message="User already in the list")

#Aborts the extraction of a reaction role's data if the reaction role's ID isn't in the list.
def abort_if_reacrole_id_doesnt_exist(reacrole_id):
	for i in range(len(reaction_roles)):
		if reacrole_id == reaction_roles[i]["ID"]:
			return #In that case the ID is found here, so there's no need to go and search for it any longer
			
	abort(404, message="Invalid reaction role ID")

#Aborts the insertion of a reaction role's data if the reaction role's ID already exists.
def abort_if_reacrole_id_already_exists(reacrole_id):
	for i in range(len(reaction_roles)):
		if reacrole_id == reaction_roles[i]["ID"]:
			abort(409, message="Reaction role already in the list")

#Aborts the extraction of a command's data if the command's ID isn't in the list.
def abort_if_command_id_doesnt_exist(command_id):
	for i in range(len(commands)):
		if command_id == commands[i]["ID"]:
			return #In that case the ID is found here, so there's no need to go and search for it any longer

	abort(404, message="Invalid command ID")

#Aborts the insertion of a command's data if the command's ID already exists.
def abort_if_command_id_already_exists(command_id):
	for i in range(len(commands)):
		if command_id in commands[i]["ID"]:
			abort(409, messag="Command already in the list")

#Abort the extraction of a character's data if the character's ID isn't in the list.
def abort_if_character_id_doesnt_exist(char_id):
	for i in range(len(characters)):
		if char_id == characters[i]["ID"]:
			return #In that case the ID is found here, so there's no need to go and search for it any longer
	
	abort(404, message="Invalid character ID")

#Abort the insertion of a character's data if the character's ID already exists.
def abort_if_character_id_already_exists(char_id):
	for i in range(len(characters)):
		if char_id == characters[i]["ID"]:
			abort(409, message="Character already in the list")

#Abort the extraction of a stats' data if the stats' ID isn't in the list.
def abort_if_stats_id_doesnt_exist(stats_id):
	for i in range(len(stats)):
		if stats_id == stats[i]["ID"]:
			return #In that case the ID is found here, so there's no need to go and search for it any longer
	
	abort(404, message="Invalid stats ID")

#Abort the insertion of a stats' data if the stats' ID already exists.
def abort_if_stats_id_already_exists(stats_id):
	for i in range(len(stats)):
		if stats_id == stats[i]["ID"]:
			abort(409, message="Stats already in the list")

#----------------
# Editing methods
#----------------

#This method is pretty much here because I thought it would be ugly to leave an
#endless list of 'if' in the Server put method.
#At the moment, I can't think of a real better way to do that, but it might be solved
#in the near future, via an HTTP request that will allow the modification of only one
#parameter. This way we will only have to create a switch/case to check which parameter
#needs to be modified, and we won't have to deal with JSON parsing in Java anymore.
#I'm also very likely to create methods that will edit several predefined parameters
#at once, as it would reduce the amount of simultaneous requests to the API. 
def edit_server(i, args) :
	#if there is a value in the users field
	if args["users"] != None :
		servers[i]["users"].append(args["users"]) #Not sure about that syntax!!

	#if there is a value in the maxWarn field
	if args["maxWarn"] != None : 
		servers[i]["maxWarn"] = args["maxWarn"]

	#if there is a value in the cooldown field
	if args["cooldown"] != None :
		servers[i]["cooldown"] = args["cooldown"]

	#if there is a value in the banned field
	if args["banned"] != None :
		servers[i]["banned"].append(args["banned"]) #Not sure about that syntax!!

	#if there is a value in the prefix field
	if args["prefix"] != None :
		servers[i]["prefix"] = args["prefix"]
	
	#if there is a value in the autoRoles field
	if args["autoRoles"] != None :
		servers[i]["autoRoles"].append(args["autoRoles"]) #Not sure about that syntax!!

	#if there is a value in the reactionRoles field
	if args["reactionRoles"] != None :
		servers[i]["reactionRoles"].append(args["reactionRoles"]) #Not sure about that syntax!!
	
	#if there is a value in the customCommands field
	if args["customCommands"] != None :
		servers[i]["customCommands"].append(args["customCommands"]) #Not sure about that syntax!!

#-----------------------------------
# Controllers to handle the requests
#-----------------------------------

#We define the controller for a request POST at the address /servers
#It will allow the creation of new servers, which will automatically
#be done by the bot itself, when he joins a new server
class Servers(Resource) :
	def post(self) :
		#We check that the args of the POST request matches the request parser created above
		args = serv_post_args.parse_args()

		#Cancel the request if the server already exists in the list
		abort_if_server_id_already_exists(args["ID"])
		servers.append(args)

		#We re-write the whole JSON file to store the current data
		#WARNING!! This is highly unefficient. Since this bot is mostly only going to be on
		#one or two servers, it is not a real problem. However, if the amount of servers it
		#gets to be on increases a lot, I will have to consider changing the export of data
		#to a propoer database!!
		with open(SERVERS, "w") as f:
			json.dump(servers, f)

		#Finally, we return the amount of servers in the list, along with a 201 HTTP code.
		#The return could be changed to anything, it is just indicative. I'll see later in
		#the development if I need it to return a particular kind of data.
		return len(servers), 201

api.add_resource(Servers, "/servers")

#We define the controller for GET, PUT and DELETE resquests, at the
#address /server/<int:server_id>. The server ID will be the one provided
#by discord itself.
#It will allow the modification of a server (when you wanna change the
#prefix for instance), its deletion (when the bot leaves a server) and
#the data retrieval.
#-------
# NOTE :
#The GET method will return the whole JSON part of a server. It might be
#a bit bothering for data retrieval since the bot will be made in Java
#and Java doesn't read Json natively. I might consider developping other
#controllers that will only return the desired value in the future.
class Server(Resource) :
	def get(self, server_id) :
		#We cancel the request if the server ID requested is not in the list.
		#On the other hand, if the server is effectively in the list, we get its index back.
		i = abort_if_server_id_doesnt_exist(server_id)

		#Then we return the JSON part for this exact server, along with a 200 HTTP code.
		return servers[i], 200

	def put(self, server_id) :
		#We cancel the request directly if the server isn't in the list. That will ensure we do
		#not consume operations to verify the request's correctness if it can only end aborted.
		#On the other hand, if the server is effectively in the list, we get its index back.
		i = abort_if_server_id_doesnt_exist(server_id)

		#Then we verirfy the args of the PUT method, to ensure they respect the parser defined
		#above, and we parse them if they do.
		args = serv_put_args.parse_args()

		#Here we look at which args have been edited, and we change their value in the server.
		edit_server(i, args)

		#We re-write the whole JSON file to store the freshly edited data
		#WARNING!! This is highly unefficient. Since this bot is mostly only going to be on
		#one or two servers, it is not a real problem. However, if the amount of servers it
		#gets to be on increases a lot, I will have to consider changing the export of data
		#to a propoer database!!
		with open(SERVERS, "w") as f :
			json.dump(servers, f)

		#Finally, we return the server modified, along with a 200 HTTP code.
		return servers[i], 200

	def delete(self, server_id) :
		#Same as the put request, if the server isn't found in the list, we abort directly the
		#operation.
		#Otherwise we get the index of the server and delete it from the list.
		i = abort_if_server_id_doesnt_exist(server_id)
		del servers[i]

		#We re-write the whole JSON file once again to delete the server's data
		#WARNING!! This is highly unefficient. Since this bot is mostly only going to be on
		#one or two servers, it is not a real problem. However, if the amount of servers it
		#gets to be on increases a lot, I will have to consider changing the export of data
		#to a propoer database!!
		with open(SERVERS, "w") as f :
			json.dump(servers, f)

		#Finally, we return the new length of the list, along with a 200 HTTP code.
		return len(servers), 200

api.add_resource(Server, "/server/<int:server_id>")

#We define the controller for a request GET at the address /users
#It will return the whole list of users it knows.
#-------
# NOTE :
#This request is dangerous in terms of privacy, so if it is not needed,
#we will consider removing it from the API!!
class Users(Resource) :
	def get(self) :
		return users

api.add_resource(Users, "/users")

#We define the controller for a request GET at the address /reaction_role
#It will return the whole list of reaction roles.
class ReactionRoles(Resource) :
	def get(self) :
		return reaction_roles

api.add_resource(ReactionRoles, "/reaction_roles")

#We define the controller for a request GET at the address /commands
#It will return the whole list of commands.
class Commands(Resource) :
	def get(self) :
		return commands

api.add_resource(Commands, "/commands")

#We define the controller for a request GET at the address /characters
#It will return the whole list of characters.
class Characters(Resource) :
	def get(self) :
		return characters

api.add_resource(Characters, "/characters")

#We define the controller for a request GET at the address /stats
#It will return the whole list of stats.
class Stats(Resource) :
	def get(self) :
		return stats

api.add_resource(Stats, "/stats")

if __name__ == "__main__" :
	app.run(debug = True)