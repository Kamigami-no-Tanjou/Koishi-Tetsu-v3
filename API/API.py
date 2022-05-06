from ast import arguments
from urllib import request
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
WARNINGS = "./DATA/WARNINGS.json"


#-----------------------------------------------------------------------------------------
# We start by defining the request parsers for the different requests that needs one.
# A request parser allows us to define the different attributes that we want in a request.
#-----------------------------------------------------------------------------------------

#request parser for a POST request on the server list :
serv_post_args = reqparse.RequestParser()
serv_post_args.add_argument("ID", type=int, required=True)
serv_post_args.add_argument("mutedUsers", type = int, default=[], action='append')
serv_post_args.add_argument("mutedRole", type=int, default=0)
serv_post_args.add_argument("maxWarn", type=int, default=3)
serv_post_args.add_argument("cooldown", type=int, default=150)
serv_post_args.add_argument("banned", type=int, default=[], action='append')
serv_post_args.add_argument("warnings", type=int, default=[], action='append')
serv_post_args.add_argument("prefix", type=str, default='kt')
serv_post_args.add_argument("autoRoles", type=int, default=[], action='append')
serv_post_args.add_argument("reactionRoles", type=int, default=[], action='append')
serv_post_args.add_argument("customCommands", type=int, default=[], action='append')

#request paresr for a PUT request on the server list :
serv_put_args = reqparse.RequestParser()
serv_put_args.add_argument("mutedUsers", type=int, action='append')
serv_put_args.add_argument("mutedRole", type=int)
serv_put_args.add_argument("maxWarn", type=int)
serv_put_args.add_argument("cooldown", type=int)
serv_put_args.add_argument("banned", type=int, action='append')
serv_put_args.add_argument("warnings", type=int, action='append')
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
user_post_args.add_argument("servers", type=int, default=[], action='append')
user_post_args.add_argument("characters", type=int, default=[], action='append')
user_post_args.add_argument("exp", type=int, default=0)
user_post_args.add_argument("birthdate", type=str, default="")

#request parser for a PUT request on the user list :
user_put_args = reqparse.RequestParser()
user_put_args.add_argument("servers", type=int, action='append')
user_put_args.add_argument("characters", type=int, action='append')
user_put_args.add_argument("exp", type=int)
user_put_args.add_argument("birthdate", type=str)

#We create a list of users and add the content of the ./DATA/USERS.json to it.
with open(USERS, "r") as rf:
	users = json.load(rf)

#request parser for a POST request on the reaction role list :
reacrole_post_args = reqparse.RequestParser()
reacrole_post_args.add_argument("message", type=int, required=True)
reacrole_post_args.add_argument("role", type=int, required=True)
reacrole_post_args.add_argument("emote", type=str, required=True)

#request parser for a PUT request on the reaction role list :
reacrole_put_args = reqparse.RequestParser()
reacrole_put_args.add_argument("message", type=int)
reacrole_put_args.add_argument("role", type=int)
reacrole_put_args.add_argument("emote", type=str)

#We create a list of reaction roles and add the content of the ./DATA/REACTIONROLES.json to it.
with open(REACTION_ROLES, "r") as rf:
	reaction_roles = json.load(rf)

#request parser for a POST request on the command list :
commands_post_args = reqparse.RequestParser()
commands_post_args.add_argument("name", type=str, required=True)
commands_post_args.add_argument("output", type=str, required=True)

#request parser for a PUT request on the command list :
commands_put_args = reqparse.RequestParser()
commands_put_args.add_argument("name", type=str)
commands_put_args.add_argument("output", type=str)

#We create a list of commands and add the content of the ./DATA/COMMANDS.json to it.
with open(COMMANDS, "r") as rf:
	commands = json.load(rf)

#request parser for a POST request on the character list :
char_post_args = reqparse.RequestParser()
char_post_args.add_argument("firstname", type=str)
char_post_args.add_argument("lastname", type=str)
char_post_args.add_argument("genre", type=str)
char_post_args.add_argument("specie", type=str)
char_post_args.add_argument("class", type=str)
char_post_args.add_argument("alignment", type=str)
char_post_args.add_argument("beliefs", type=str)
char_post_args.add_argument("stats", type=int, action='append')
char_post_args.add_argument("equipment", type=str)
char_post_args.add_argument("spells", type=str)
char_post_args.add_argument("image", type=str)

#request parser for a PUT request on the character list :
char_put_args = reqparse.RequestParser()
char_put_args.add_argument("firstname", type=str)
char_put_args.add_argument("lastname", type=str)
char_put_args.add_argument("genre", type=str)
char_put_args.add_argument("specie", type=str)
char_put_args.add_argument("class", type=str)
char_put_args.add_argument("alignment", type=str)
char_put_args.add_argument("beliefs", type=str)
char_put_args.add_argument("stats", type=int, action='append')
char_put_args.add_argument("equipment", type=str)
char_put_args.add_argument("spells", type=str)
char_put_args.add_argument("image", type=str)

#We create a list of characters and add the content of the ./DATA/CHARACTERS.json to it.
with open(CHARACTERS, "r") as rf:
	characters = json.load(rf)

#request parser for a POST request on the stats list :
stats_post_args = reqparse.RequestParser()
stats_post_args.add_argument("name", type=str, required=True)
stats_post_args.add_argument("value", type=int, required=True)

#request parser for a PUT request on the stats list :
stats_put_args = reqparse.RequestParser()
stats_put_args.add_argument("name", type=str)
stats_put_args.add_argument("value", type=int)

#We create a list of stats and add the content of the ./DATA/STATS.json to it.
with open(STATS, "r") as rf:
	stats = json.load(rf)

#request parser for a POST request on the warnings list :
warnings_post_args = reqparse.RequestParser()
warnings_post_args.add_argument("user", type=int, required=True)

#We create a list of warnings and add the content of the ./DATA/WARNINGS.json to it.
with open(WARNINGS, "r") as rf :
	warnings = json.load(rf)

#-------------------------------
# Existence verification methods
#-------------------------------

#Aborts the extraction of a server's data if the server's ID isn't in the list.
def abort_if_server_id_doesnt_exist(server_id):
	for i in range(len(servers)):
		if server_id == servers[i]["ID"]:
			#In that case the ID is found here, so there's no need to go and search for it any longer.
			#Still we return the index, for efficiency, hence we don't have to go through the whole
			#list once again.
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
			#In that case the ID is found here, so there's no need to go and search for it any longer.
			#Still we return the index, for efficiency, hence we don't have to go through the whole
			#list once again.
			return i
	
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
			#In that case the ID is found here, so there's no need to go and search for it any longer.
			#Still we return the index, for efficiency, hence we don't have to go through the whole
			#list once again.
			return i
			
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
			#In that case the ID is found here, so there's no need to go and search for it any longer.
			#Still we return the index, for efficiency, hence we don't have to go through the whole
			#list once again.
			return i

	abort(404, message="Invalid command ID")

#Aborts the insertion of a command's data if the command's ID already exists.
def abort_if_command_id_already_exists(command_id):
	for i in range(len(commands)):
		if command_id == commands[i]["ID"]:
			abort(409, messag="Command already in the list")

#Abort the extraction of a character's data if the character's ID isn't in the list.
def abort_if_character_id_doesnt_exist(char_id):
	for i in range(len(characters)):
		if char_id == characters[i]["ID"]:
			#In that case the ID is found here, so there's no need to go and search for it any longer.
			#Still we return the index, for efficiency, hence we don't have to go through the whole
			#list once again.
			return i
	
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
			#In that case the ID is found here, so there's no need to go and search for it any longer.
			#Still we return the index, for efficiency, hence we don't have to go through the whole
			#list once again.
			return i
	
	abort(404, message="Invalid stats ID")

#Abort the insertion of a stats' data if the stats' ID already exists.
def abort_if_stats_id_already_exists(stats_id):
	for i in range(len(stats)):
		if stats_id == stats[i]["ID"]:
			abort(409, message="Stats already in the list")

#Abort the extraction of a warning's data if the warning's ID isn't in the list.
def abort_if_warning_id_doesnt_exist(warning_id):
	for i in range(len(warnings)):
		if warning_id == warnings[i]["ID"]:
			#In that case the ID is found here, so there's no need to go and search for it any longer.
			#Still we return the index, for efficiency, hence we don't have to go through the whole
			#list once again.
			return i
	abort(404, message="Invalid warning ID")

#Abort the insertion of a warning's data if the warning's ID already exists.
def abort_if_warning_id_already_exists(warning_id):
	for i in range(len(warnings)):
		if warning_id == warnings[i]["ID"]:
			abort(409, message="Warning already in the list")

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
	#if there is a value in the mutedUsers field
	if args["mutedUsers"] != None :
		servers[i]["mutedUsers"].extend(args["mutedUsers"])

	#if there is a value in the mutedRole field
	if args["mutedRole"] != None :
		servers[i]["mutedRole"] = args["mutedRole"]

	#if there is a value in the maxWarn field
	if args["maxWarn"] != None : 
		servers[i]["maxWarn"] = args["maxWarn"]

	#if there is a value in the cooldown field
	if args["cooldown"] != None :
		servers[i]["cooldown"] = args["cooldown"]

	#if there is a value in the banned field
	if args["banned"] != None :
		servers[i]["banned"].extend(args["banned"])

	#if there is a value in the warnings field
	if args["warnings"] != None :
		servers[i]["warnings"].extend(args["warnings"])

	#if there is a value in the prefix field
	if args["prefix"] != None :
		servers[i]["prefix"] = args["prefix"]
	
	#if there is a value in the autoRoles field
	if args["autoRoles"] != None :
		servers[i]["autoRoles"].extend(args["autoRoles"])

	#if there is a value in the reactionRoles field
	if args["reactionRoles"] != None :
		servers[i]["reactionRoles"].extend(args["reactionRoles"])
	
	#if there is a value in the customCommands field
	if args["customCommands"] != None :
		servers[i]["customCommands"].extend(args["customCommands"])

#This method is pretty much here because I thought it would be ugly to leave an
#endless list of 'if' in the User put method.
#At the moment, I can't think of a real better way to do that, but it might be solved
#in the near future, via an HTTP request that will allow the modification of only one
#parameter. This way we will only have to create a switch/case to check which parameter
#needs to be modified, and we won't have to deal with JSON parsing in Java anymore.
#I'm also very likely to create methods that will edit several predefined parameters
#at once, as it would reduce the amount of simultaneous requests to the API. 
def edit_user(i, args) :
	#if there is a value in the servers field
	if args["servers"] != None :
		users[i]["servers"].extend(args["servers"])

	#if there is a value in the characters field
	if args["characters"] != None :
		users[i]["characters"].extend(args["characters"])

	#if there is a value in the exp field
	if args["exp"] != None : 
		users[i]["exp"] = args["exp"]

	#if there is a value in the birthdate field
	if args["birthdate"] != None :
		users[i]["birthdate"] = args["birthdate"]

#This method is pretty much here because I thought it would be ugly to leave an
#endless list of 'if' in the ReactionRole put method.
#At the moment, I can't think of a real better way to do that, but it might be solved
#in the near future, via an HTTP request that will allow the modification of only one
#parameter. This way we will only have to create a switch/case to check which parameter
#needs to be modified, and we won't have to deal with JSON parsing in Java anymore.
#I'm also very likely to create methods that will edit several predefined parameters
#at once, as it would reduce the amount of simultaneous requests to the API. 
def edit_reacrole(i, args) :
	#if there is a value in the message field
	if args["message"] != None :
		reaction_roles[i]["message"] = args["message"]

	#if there is a value in the role field
	if args["role"] != None :
		reaction_roles[i]["role"] = args["role"]

	#if there is a value in the emote field
	if args["emote"] != None : 
		reaction_roles[i]["emote"] = args["emote"]

#This method is pretty much here because I thought it would be ugly to leave an
#endless list of 'if' in the Command put method.
#At the moment, I can't think of a real better way to do that, but it might be solved
#in the near future, via an HTTP request that will allow the modification of only one
#parameter. This way we will only have to create a switch/case to check which parameter
#needs to be modified, and we won't have to deal with JSON parsing in Java anymore.
#I'm also very likely to create methods that will edit several predefined parameters
#at once, as it would reduce the amount of simultaneous requests to the API. 
def edit_command(i, args) :
	#if there is a value in the name field
	if args["name"] != None :
		commands[i]["name"] = args["name"]

	#if there is a value in the output field
	if args["output"] != None : 
		commands[i]["output"] = args["output"]

#This method is pretty much here because I thought it would be ugly to leave an
#endless list of 'if' in the Character put method.
#At the moment, I can't think of a real better way to do that, but it might be solved
#in the near future, via an HTTP request that will allow the modification of only one
#parameter. This way we will only have to create a switch/case to check which parameter
#needs to be modified, and we won't have to deal with JSON parsing in Java anymore.
#I'm also very likely to create methods that will edit several predefined parameters
#at once, as it would reduce the amount of simultaneous requests to the API. 
def edit_character(i, args) :
	#if there is a value in the firstname field
	if args["firstname"] != None :
		characters[i]["firstname"] = args["firstname"]

	#if there is a value in the lastname field
	if args["lastname"] != None : 
		characters[i]["lastname"] = args["lastname"]

	#if there is a value in the genre field
	if args["genre"] != None :
		characters[i]["genre"] = args["genre"]

	#if there is a value in the specie field
	if args["specie"] != None :
		characters[i]["specie"] = args["specie"]

	#if there is a value in the class field
	if args["class"] != None :
		characters[i]["class"] = args["class"]

	#if there is a value in the alignment field
	if args["alignment"] != None :
		characters[i]["alignment"] = args["alignment"]

	#if there is a value in the beliefs field
	if args["beliefs"] != None :
		characters[i]["beliefs"] = args["beliefs"]

	#if there is a value in the stats field
	if args["stats"] != None :
		characters[i]["stats"] = args["stats"]

	#if there is a value in the equipment field
	if args["equipment"] != None :
		characters[i]["equipment"] = args["equipment"]

	#if there is a value in the spells field
	if args["spells"] != None :
		characters[i]["spells"] = args["spells"]

	#if there is a value in the image field
	if args["image"] != None :
		characters[i]["image"] = args["image"]

#This method is pretty much here because I thought it would be ugly to leave an
#endless list of 'if' in the Stat put method.
#At the moment, I can't think of a real better way to do that, but it might be solved
#in the near future, via an HTTP request that will allow the modification of only one
#parameter. This way we will only have to create a switch/case to check which parameter
#needs to be modified, and we won't have to deal with JSON parsing in Java anymore.
#I'm also very likely to create methods that will edit several predefined parameters
#at once, as it would reduce the amount of simultaneous requests to the API. 
def edit_stat(i, args) :
	#if there is a value in the name field
	if args["name"] != None :
		stats[i]["name"] = args["name"]

	#if there is a value in the value field
	if args["value"] != None : 
		stats[i]["value"] = args["value"]

#-----------------------------------
# Controllers to handle the requests
#-----------------------------------

#We define the controller for a request POST at the address /servers
#It will allow the creation of new servers, which will automatically
#be done by the bot itself, when he joins a new server
class Servers(Resource) :
	def post(self) :
		#We check that the args of the POST request matches the request parser created above
		server = serv_post_args.parse_args()

		#Cancel the request if the server already exists in the list
		abort_if_server_id_already_exists(server["ID"])
		servers.append(server)

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

#We define the controller for a request POST at the address /users
#It will allow the creation of new users, which will automatically
#be done by the bot itself, when he recieves a message from that
#user
class Users(Resource) :
	def post(self) :
		#We check that the args of the POST request matches the request parser created above
		user = user_post_args.parse_args()

		#Cancel the request if the user already exists in the list
		abort_if_user_id_already_exists(user["ID"])
		users.append(user)

		#We re-write the whole JSON file to store the current data
		#WARNING!! This is highly unefficient. Since this bot is mostly only going to be on
		#one or two servers, it is not a real problem. However, if the amount of servers it
		#gets to be on increases a lot, I will have to consider changing the export of data
		#to a propoer database!!
		with open(USERS, "w") as f:
			json.dump(users, f)

		#Finally, we return the amount of users in the list, along with a 201 HTTP code.
		#The return could be changed to anything, it is just indicative. I'll see later in
		#the development if I need it to return a particular kind of data.
		return len(users), 201

api.add_resource(Users, "/users")

#We define the controller for GET, PUT and DELETE resquests, at the
#address /user/<int:user_id>. The user ID will be the one provided
#by discord itself.
#It will allow the modification of a user (when you warn him for
#instance), its deletion (when he asks for his data to be deleted)
#and the data retrieval.
#-------
# NOTE :
#The GET method will return the whole JSON part of a user. It might be
#a bit bothering for data retrieval since the bot will be made in Java
#and Java doesn't read Json natively. I might consider developping other
#controllers that will only return the desired value in the future.
class User(Resource) :
	def get(self, user_id) :
		#We cancel the request if the user ID requested is not in the list.
		#On the other hand, if the user is effectively in the list, we get its index back.
		i = abort_if_user_id_doesnt_exist(user_id)

		#Then we return the JSON part for this exact user, along with a 200 HTTP code.
		return users[i], 200

	def put(self, user_id) :
		#We cancel the request directly if the user isn't in the list. That will ensure we do
		#not consume operations to verify the request's correctness if it can only end aborted.
		#On the other hand, if the user is effectively in the list, we get its index back.
		i = abort_if_user_id_doesnt_exist(user_id)

		#Then we verirfy the args of the PUT method, to ensure they respect the parser defined
		#above, and we parse them if they do.
		args = user_put_args.parse_args()

		#Here we look at which args have been edited, and we change their value in the user.
		edit_user(i, args)

		#We re-write the whole JSON file to store the freshly edited data
		#WARNING!! This is highly unefficient. Since this bot is mostly only going to be on
		#one or two servers, it is not a real problem. However, if the amount of servers it
		#gets to be on increases a lot, I will have to consider changing the export of data
		#to a propoer database!!
		with open(USERS, "w") as f :
			json.dump(users, f)

		#Finally, we return the user modified, along with a 200 HTTP code.
		return users[i], 200

	def delete(self, user_id) :
		#Same as the put request, if the user isn't found in the list, we abort directly the
		#operation.
		#Otherwise we get the index of the user and delete him from the list.
		i = abort_if_user_id_doesnt_exist(user_id)
		del users[i]

		#We re-write the whole JSON file once again to delete the user's data
		#WARNING!! This is highly unefficient. Since this bot is mostly only going to be on
		#one or two servers, it is not a real problem. However, if the amount of servers it
		#gets to be on increases a lot, I will have to consider changing the export of data
		#to a propoer database!!
		with open(USERS, "w") as f :
			json.dump(users, f)

		#Finally, we return the new length of the list, along with a 200 HTTP code.
		return len(users), 200

api.add_resource(User, "/user/<int:user_id>")

#We define the controller for POST and GET requests at the address
#/reaction_role
#It will allow the creation of new reaction roles and return the whole
#list of reaction roles.
class ReactionRoles(Resource) :
	def get(self) :
		return reaction_roles

	def post(self) :
		#We check that the args of the POST request matches the request parser created above
		args = reacrole_post_args.parse_args()

		#We create the dictionnary for a reaction role and we give it its id. We then
		#increment the variable by one to keep the count correct
		id = reaction_roles[len(reaction_roles) - 1]["ID"] + 1
		reaction_role = {"ID" : id}

		#We add to that dictionnary the args recieved from the request
		reaction_role.update(args)

		#Just in case, we cancel the request if the id given already exists in the list
		abort_if_reacrole_id_already_exists(reaction_role["ID"])
		reaction_roles.append(reaction_role)

		#We re-write the whole JSON file to store the current data
		#WARNING!! This is highly unefficient. Since this bot is mostly only going to be on
		#one or two servers, it is not a real problem. However, if the amount of servers it
		#gets to be on increases a lot, I will have to consider changing the export of data
		#to a propoer database!!
		with open(REACTION_ROLES, "w") as f:
			json.dump(reaction_roles, f)

		#Finally, we return its ID, as it can't be known above, along with a 201 HTTP code.
		return reaction_role["ID"], 201

api.add_resource(ReactionRoles, "/reaction_roles")

#We define the controller for GET, PUT and DELETE resquests, at the
#address /reaction_role/<int:reacrole_id>. The reaction role ID will
#be arbitrarily provided by the API itself.
#It will allow the modification of a reaction role (when you change
#the emote for instance), its deletion and the data retrieval.
#-------
# NOTE :
#The GET method will return the whole JSON part of a reaction role. It 
#might be a bit bothering for data retrieval since the bot will be made
#in Java and Java doesn't read Json natively. I might consider developping
#other controllers that will only return the desired value in the future.
class ReactionRole(Resource) :
	def get(self, reacrole_id) :
		#We cancel the request if the reaction role ID requested is not in the list.
		#On the other hand, if the reaction role is effectively in the list, we get
		#its index back.
		i = abort_if_reacrole_id_doesnt_exist(reacrole_id)

		#Then we return the JSON part for this exact reaction role, along with a 200 HTTP code.
		return reaction_roles[i], 200

	def put(self, reacrole_id) :
		#We cancel the request directly if the reaction role isn't in the list. That will ensure
		#we do not consume operations to verify the request's correctness if it can only end
		#aborted.
		#On the other hand, if the reaction role is effectively in the list, we get its index
		#back.
		i = abort_if_reacrole_id_doesnt_exist(reacrole_id)

		#Then we verirfy the args of the PUT method, to ensure they respect the parser defined
		#above, and we parse them if they do.
		args = reacrole_put_args.parse_args()

		#Here we look at which args have been edited, and we change their value in the reaction
		#role.
		edit_reacrole(i, args)

		#We re-write the whole JSON file to store the freshly edited data
		#WARNING!! This is highly unefficient. Since this bot is mostly only going to be on
		#one or two servers, it is not a real problem. However, if the amount of servers it
		#gets to be on increases a lot, I will have to consider changing the export of data
		#to a propoer database!!
		with open(REACTION_ROLES, "w") as f :
			json.dump(reaction_roles, f)

		#Finally, we return the reaction role modified, along with a 200 HTTP code.
		return reaction_roles[i], 200

	def delete(self, reacrole_id) :
		#Same as the put request, if the reaction role isn't found in the list, we abort
		#directly the operation.
		#Otherwise we get the index of the reaction role and delete it from the list.
		i = abort_if_reacrole_id_doesnt_exist(reacrole_id)
		del reaction_roles[i]

		#We re-write the whole JSON file once again to delete the reaction role's data
		#WARNING!! This is highly unefficient. Since this bot is mostly only going to be on
		#one or two servers, it is not a real problem. However, if the amount of servers it
		#gets to be on increases a lot, I will have to consider changing the export of data
		#to a propoer database!!
		with open(REACTION_ROLES, "w") as f :
			json.dump(reaction_roles, f)

		#Finally, we return the new length of the list, along with a 200 HTTP code.
		return len(reaction_roles), 200

api.add_resource(ReactionRole, "/reaction_role/<int:reacrole_id>")

#We define the controller for POST and GET requests at the address /comamnds
#It will allow the creation of new reaction roles and return the whole list of 
#commands.
class Commands(Resource) :
	def get(self) :
		return commands

	def post(self) :
		#We check that the args of the POST request matches the request parser created above
		args = commands_post_args.parse_args()

		#We create the dictionnary for a command and we give it its id. We then increment
		#the variable by one to keep the count correct
		id = commands[len(commands) - 1]["ID"] + 1
		command = {"ID" : id}

		#We add to that dictionnary the args recieved from the request
		command.update(args)

		#Just in case, we cancel the request if the id given already exists in the list
		abort_if_command_id_already_exists(command["ID"])
		commands.append(command)

		#We re-write the whole JSON file to store the current data
		#WARNING!! This is highly unefficient. Since this bot is mostly only going to be on
		#one or two servers, it is not a real problem. However, if the amount of servers it
		#gets to be on increases a lot, I will have to consider changing the export of data
		#to a propoer database!!
		with open(COMMANDS, "w") as f:
			json.dump(commands, f)

		#Finally, we return its ID, as it can't be known above, along with a 201 HTTP code.
		return command["ID"], 201

api.add_resource(Commands, "/commands")

#We define the controller for GET, PUT and DELETE resquests, at the
#address /command/<int:command_id>. The command ID will be arbitrarily
#provided by the API itself.
#It will allow the modification of a command (when you want to change
#its output for instance), its deletion and the data retrieval.
#-------
# NOTE :
#The GET method will return the whole JSON part of a command. It might be
#a bit bothering for data retrieval since the bot will be made in Java
#and Java doesn't read Json natively. I might consider developping other
#controllers that will only return the desired value in the future.
class Command(Resource) :
	def get(self, command_id) :
		#We cancel the request if the command ID requested is not in the list.
		#On the other hand, if the command is effectively in the list, we get its
		#index back.
		i = abort_if_command_id_doesnt_exist(command_id)

		#Then we return the JSON part for this exact command, along with a 200 HTTP code.
		return commands[i], 200

	def put(self, command_id) :
		#We cancel the request directly if the command isn't in the list. That will ensure we
		#do not consume operations to verify the request's correctness if it can only end
		#aborted.
		#On the other hand, if the command is effectively in the list, we get its index back.
		i = abort_if_command_id_doesnt_exist(command_id)

		#Then we verirfy the args of the PUT method, to ensure they respect the parser defined
		#above, and we parse them if they do.
		args = commands_put_args.parse_args()

		#Here we look at which args have been edited, and we change their value in the command
		edit_command(i, args)

		#We re-write the whole JSON file to store the freshly edited data
		#WARNING!! This is highly unefficient. Since this bot is mostly only going to be on
		#one or two servers, it is not a real problem. However, if the amount of servers it
		#gets to be on increases a lot, I will have to consider changing the export of data
		#to a propoer database!!
		with open(COMMANDS, "w") as f :
			json.dump(commands, f)

		#Finally, we return the command modified, along with a 200 HTTP code.
		return commands[i], 200

	def delete(self, command_id) :
		#Same as the put request, if the command isn't found in the list, we abort directly
		#the operation.
		#Otherwise we get the index of the command and delete it from the list.
		i = abort_if_command_id_doesnt_exist(command_id)
		del commands[i]

		#We re-write the whole JSON file once again to delete the command's data
		#WARNING!! This is highly unefficient. Since this bot is mostly only going to be on
		#one or two servers, it is not a real problem. However, if the amount of servers it
		#gets to be on increases a lot, I will have to consider changing the export of data
		#to a propoer database!!
		with open(COMMANDS, "w") as f :
			json.dump(commands, f)

		#Finally, we return the new length of the list, along with a 200 HTTP code.
		return len(commands), 200

api.add_resource(Command, "/command/<int:command_id>")

#We define the controller for POST and GET requests at the address /characters
#It will allow the creation of new characters and return the whole list of
#characters.
class Characters(Resource) :
	def get(self) :
		return characters

	def post(self) :
		#We check that the args of the POST request matches the request parser created above
		args = char_post_args.parse_args()

		#We create the dictionnary for a command and we give it its id. We then increment
		#the variable by one to keep the count correct
		id = characters[len(characters) - 1]["ID"] + 1
		character = {"ID" : id}

		#We add to that dictionnary the args recieved from the request
		character.update(args)

		#Just in case, we cancel the request if the id given already exists in the list
		abort_if_character_id_already_exists(character["ID"])
		characters.append(character)

		#We re-write the whole JSON file to store the current data
		#WARNING!! This is highly unefficient. Since this bot is mostly only going to be on
		#one or two servers, it is not a real problem. However, if the amount of servers it
		#gets to be on increases a lot, I will have to consider changing the export of data
		#to a propoer database!!
		with open(CHARACTERS, "w") as f:
			json.dump(characters, f)

		#Finally, we return its ID, as it can't be known above, along with a 201 HTTP code.
		return character["ID"], 201

api.add_resource(Characters, "/characters")

#We define the controller for GET, PUT and DELETE resquests, at the
#address /character/<int:character_id>. The character ID will be
#arbitrarily provided by the API itself.
#It will allow the modification of a character (when you want to change
#its name, class, etc, etc...), its deletion and the data retrieval.
#-------
# NOTE :
#The GET method will return the whole JSON part of a character. It might be
#a bit bothering for data retrieval since the bot will be made in Java
#and Java doesn't read Json natively. I might consider developping other
#controllers that will only return the desired value in the future.
class Character(Resource) :
	def get(self, character_id) :
		#We cancel the request if the character ID requested is not in the list.
		#On the other hand, if the character is effectively in the list, we get its
		#index back.
		i = abort_if_character_id_doesnt_exist(character_id)

		#Then we return the JSON part for this exact character, along with a 200 HTTP code.
		return characters[i], 200

	def put(self, character_id) :
		#We cancel the request directly if the character isn't in the list. That will ensure we
		#do not consume operations to verify the request's correctness if it can only end
		#aborted.
		#On the other hand, if the character is effectively in the list, we get its index back.
		i = abort_if_character_id_doesnt_exist(character_id)

		#Then we verirfy the args of the PUT method, to ensure they respect the parser defined
		#above, and we parse them if they do.
		args = char_put_args.parse_args()

		#Here we look at which args have been edited, and we change their value in the character
		edit_character(i, args)

		#We re-write the whole JSON file to store the freshly edited data
		#WARNING!! This is highly unefficient. Since this bot is mostly only going to be on
		#one or two servers, it is not a real problem. However, if the amount of servers it
		#gets to be on increases a lot, I will have to consider changing the export of data
		#to a propoer database!!
		with open(CHARACTERS, "w") as f :
			json.dump(characters, f)

		#Finally, we return the character modified, along with a 200 HTTP code.
		return characters[i], 200

	def delete(self, character_id) :
		#Same as the put request, if the character isn't found in the list, we abort directly
		#the operation.
		#Otherwise we get the index of the character and delete it from the list.
		i = abort_if_character_id_doesnt_exist(character_id)
		del characters[i]

		#We re-write the whole JSON file once again to delete the character's data
		#WARNING!! This is highly unefficient. Since this bot is mostly only going to be on
		#one or two servers, it is not a real problem. However, if the amount of servers it
		#gets to be on increases a lot, I will have to consider changing the export of data
		#to a propoer database!!
		with open(CHARACTERS, "w") as f :
			json.dump(characters, f)

		#Finally, we return the new length of the list, along with a 200 HTTP code.
		return len(characters), 200

api.add_resource(Character, "/character/<int:character_id>")

#We define the controller for POST and GET requests at the address /stats
#It will allow the creation of new stats and return the whole list of stats.
class Stats(Resource) :
	def get(self) :
		return stats

	def post(self) :
		#We check that the args of the POST request matches the request parser created above
		args = stats_post_args.parse_args()

		#We create the dictionnary for a stat and we give it its id. We then increment the
		#variable by one to keep the count correct
		id = stats[len(stats) - 1]["ID"] + 1
		stat = {"ID" : id}

		#We add to that dictionnary the args recieved from the request
		stat.update(args)

		#Just in case, we cancel the request if the id given already exists in the list
		abort_if_stats_id_already_exists(stat["ID"])
		stats.append(stat)

		#We re-write the whole JSON file to store the current data
		#WARNING!! This is highly unefficient. Since this bot is mostly only going to be on
		#one or two servers, it is not a real problem. However, if the amount of servers it
		#gets to be on increases a lot, I will have to consider changing the export of data
		#to a propoer database!!
		with open(STATS, "w") as f:
			json.dump(stats, f)

		#Finally, we return its ID, as it can't be known above, along with a 201 HTTP code.
		return stat["ID"], 201

api.add_resource(Stats, "/stats")

#We define the controller for GET, PUT and DELETE resquests, at the address
#/stat/<int:stat_id>. The stat ID will be arbitrarily provided by the API
#itself.
#It will allow the modification of a character's stat, its deletion and the
#data retrieval.
#-------
# NOTE :
#The GET method will return the whole JSON part of a stat. It might be
#a bit bothering for data retrieval since the bot will be made in Java
#and Java doesn't read Json natively. I might consider developping other
#controllers that will only return the desired value in the future.
class Stat(Resource) :
	def get(self, stat_id) :
		#We cancel the request if the stat ID requested is not in the list.
		#On the other hand, if the stat is effectively in the list, we get its
		#index back.
		i = abort_if_stats_id_doesnt_exist(stat_id)

		#Then we return the JSON part for this exact stat, along with a 200 HTTP code.
		return stats[i], 200

	def put(self, stat_id) :
		#We cancel the request directly if the stat isn't in the list. That will ensure we
		#do not consume operations to verify the request's correctness if it can only end
		#aborted.
		#On the other hand, if the stat is effectively in the list, we get its index back.
		i = abort_if_stats_id_doesnt_exist(stat_id)

		#Then we verirfy the args of the PUT method, to ensure they respect the parser defined
		#above, and we parse them if they do.
		args = stats_put_args.parse_args()

		#Here we look at which args have been edited, and we change their value in the character
		edit_stat(i, args)

		#We re-write the whole JSON file to store the freshly edited data
		#WARNING!! This is highly unefficient. Since this bot is mostly only going to be on
		#one or two servers, it is not a real problem. However, if the amount of servers it
		#gets to be on increases a lot, I will have to consider changing the export of data
		#to a propoer database!!
		with open(STATS, "w") as f :
			json.dump(stats, f)

		#Finally, we return the stat modified, along with a 200 HTTP code.
		return stats[i], 200

	def delete(self, stat_id) :
		#Same as the put request, if the stat isn't found in the list, we abort directly
		#the operation.
		#Otherwise we get the index of the stat and delete it from the list.
		i = abort_if_stats_id_doesnt_exist(stat_id)
		del stats[i]

		#We re-write the whole JSON file once again to delete the stat's data
		#WARNING!! This is highly unefficient. Since this bot is mostly only going to be on
		#one or two servers, it is not a real problem. However, if the amount of servers it
		#gets to be on increases a lot, I will have to consider changing the export of data
		#to a propoer database!!
		with open(STATS, "w") as f :
			json.dump(stats, f)

		#Finally, we return the new length of the list, along with a 200 HTTP code.
		return len(stats), 200

api.add_resource(Stat, "/stat/<int:stat_id>")

#We define the controller for a request GET at the address /warnings
#It will return the whole list of warnings.
class Warnings(Resource) :
	def get(self) :
		return warnings

	def post(self) :
		#We check that the args of the POST request matches the request parser created above
		args = warnings_post_args.parse_args()

		#We create the dictionnary for a warning and we give it its id. We then increment
		#the variable by one to keep the count correct
		id = warnings[len(warnings) - 1]["ID"] + 1
		warning = {"ID" : id}

		#We add to that dictionnary the args recieved from the request
		warning.update(args)

		#Just in case, we cancel the request if the id given already exists in the list
		abort_if_warning_id_already_exists(warning["ID"])
		warnings.append(warning)

		#We re-write the whole JSON file to store the current data
		#WARNING!! This is highly unefficient. Since this bot is mostly only going to be on
		#one or two servers, it is not a real problem. However, if the amount of servers it
		#gets to be on increases a lot, I will have to consider changing the export of data
		#to a propoer database!!
		with open(WARNINGS, "w") as f:
			json.dump(warnings, f)

		#Finally, we return its ID, as it can't be known above, along with a 201 HTTP code.
		return warning["ID"], 201

api.add_resource(Warnings, "/warnings")

#We define the controller for GET and DELETE resquests, at the address
#/warning/<int:warning_id>. The warning ID will be arbitrarily provided by the
#API itself.
#It will only allow the deletion and the data retrieval of a warning, as it
#isn't meant to be editable.
#-------
# NOTE :
#The GET method will return the whole JSON part of a stat. It might be
#a bit bothering for data retrieval since the bot will be made in Java
#and Java doesn't read Json natively. I might consider developping other
#controllers that will only return the desired value in the future.
class Warning(Resource) :
	def get(self, warning_id) :
		#We cancel the request if the warning ID requested is not in the list.
		#On the other hand, if the warning is effectively in the list, we get its
		#index back.
		i = abort_if_warning_id_doesnt_exist(warning_id)

		#Then we return the JSON part for this exact warning, along with a 200 HTTP code.
		return warnings[i], 200

	def delete(self, warning_id) :
		#If the warning isn't found in the list, we abort directly the operation.
		#Otherwise we get the index of the warning and delete it from the list.
		i = abort_if_warning_id_doesnt_exist(warning_id)
		del warnings[i]

		#We re-write the whole JSON file once again to delete the warning's data
		#WARNING!! This is highly unefficient. Since this bot is mostly only going to be on
		#one or two servers, it is not a real problem. However, if the amount of servers it
		#gets to be on increases a lot, I will have to consider changing the export of data
		#to a propoer database!!
		with open(WARNINGS, "w") as f :
			json.dump(warnings, f)

		#Finally, we return the new length of the list, along with a 200 HTTP code.
		return len(warnings), 200

api.add_resource(Warning, "/warning/<int:warning_id>")

if __name__ == "__main__" :
	app.run(debug = True)