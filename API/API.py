from numpy import char
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
from flask_cors import CORS
import json

app = Flask(__name__)
api = Api(app)
cors = CORS(app)

#-----------------------------------------------------------------------------------------
# We start by defining the request parsers for the different requests that needs one.
# A request parser allows us to define the different attributes that we want in a request.
#-----------------------------------------------------------------------------------------

#request parser for a POST request on the server list :
serv_post_args = reqparse.RequestParser()
serv_post_args.add_argument("ID", type=int, required=True)
serv_post_args.add_argument("users", action='append', required=True)
serv_post_args.add_argument("maxWarn", type=int, required=True)
serv_post_args.add_argument("cooldown", type=int, required=True)
serv_post_args.add_argument("banned", action='append')
serv_post_args.add_argument("prefix", type=str, required=True)
serv_post_args.add_argument("autoRoles", action='append')
serv_post_args.add_argument("reactionRoles", action='append')
serv_post_args.add_argument("customCommands", action='append')

#request paresr for a PUT request on the server list :
serv_put_args = reqparse.RequestParser()
serv_put_args.add_argument("ID", type=int)
serv_put_args.add_argument("users", action='append')
serv_put_args.add_argument("maxWarn", type=int)
serv_put_args.add_argument("cooldown", type=int)
serv_put_args.add_argument("banned", action='append')
serv_put_args.add_argument("prefix", type=str)
serv_put_args.add_argument("autoRoles", action='append')
serv_put_args.add_argument("reactionRoles", action='append')
serv_put_args.add_argument("customCommands", action='append')

#We create a list of servers and add the content of the ./DATA/SERVERS.json to it.
with open("./DATA/SERVERS.json", "r") as rf:
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
user_put_args.add_argument("ID", type=int)
user_put_args.add_argument("characters", action='append')
user_put_args.add_argument("muted", type=int)
user_put_args.add_argument("warnings", type=int)
user_put_args.add_argument("exp", type=int)
user_put_args.add_argument("birthdate", type=str)

#We create a list of users and add the content of the ./DATA/USERS.json to it.
with open("./DATA/USERS.json", "r") as rf:
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
with open("./DATA/REACTIONROLES.json", "r") as rf:
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
with open("./DATA/COMMANDS.json", "r") as rf:
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
with open("./DATA/CHARACTERS.json", "r") as rf:
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
with open("./DATA/STATS.json", "r") as rf:
	stats = json.load(rf)

#-------------------------------
# Existence verification methods
#-------------------------------

#Aborts the extraction of a server's data if the server's ID isn't in the list.
def abort_if_server_id_doesnt_exist(server_id):
	if server_id not in servers["ID"]:
		abort(404, message="Invalid server ID")

#Aborts the insertion of a server's data if the server's ID already exists.
def abort_if_server_id_already_exists(server_id):
	if server_id in servers["ID"]:
		abort(409, message="Server already in the list")

#Aborts the extraction of a user's data if the user's ID isn't in the list.
def abort_if_user_id_doesnt_exist(user_id):
	if user_id not in users["ID"]:
		abort(404, message="Invalid user ID")

#Aborts the insertion of a user's data if the user's ID already exists.
def abort_if_user_id_already_exists(user_id):
	if user_id in users["ID"]:
		abort(409, message="User already in the list")

#Aborts the extraction of a reaction role's data if the reaction role's ID isn't in the list.
def abort_if_reacrole_id_doesnt_exist(reacrole_id):
	if reacrole_id not in reaction_roles["ID"]:
		abort(404, message="Invalid reaction role ID")

#Aborts the insertion of a reaction role's data if the reaction role's ID already exists.
def abort_if_reacrole_id_already_exists(reacrole_id):
	if reacrole_id in reaction_roles["ID"]:
		abort(409, message="Reaction role already in the list")

#Aborts the extraction of a command's data if the command's ID isn't in the list.
def abort_if_command_id_doesnt_exist(command_id):
	if command_id not in commands["ID"]:
		abort(404, message="Invalid command ID")

#Aborts the insertion of a command's data if the command's ID already exists.
def abort_if_command_id_already_exists(command_id):
	if command_id in commands["ID"]:
		abort(409, messag="Command already in the list")

#Abort the extraction of a character's data if the character's ID isn't in the list.
def abort_if_character_id_doesnt_exist(char_id):
	if char_id not in characters["ID"]:
		abort(404, message="Invalid character ID")

#Abort the insertion of a character's data if the character's ID already exists.
def abort_if_character_id_already_exists(char_id):
	if char_id in characters["ID"]:
		abort(409, message="Character already in the list")

#Abort the extraction of a stats' data if the stats' ID isn't in the list.
def abort_if_stats_id_doesnt_exist(stats_id):
	if stats_id not in stats["ID"]:
		abort(404, message="Invalid stats ID")

#Abort the insertion of a stats' data if the stats' ID already exists.
def abort_if_stats_id_already_exists(stats_id):
	if stats_id in stats["ID"]:
		abort(409, message="Stats already in the list")

#-----------------------------------
# Controllers to handle the requests
#-----------------------------------

#We define the controller for a request GET at the address /servers
#It will return the whole list of servers it has access to.
#-------
# NOTE :
#This request is dangerous in terms of privacy, so if it is not needed,
#we will consider removing it from the API!!
class Servers(Resource) :
	def get(self) :
		return servers

api.add_resource(Servers, "/servers")

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