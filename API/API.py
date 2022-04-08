from typing_extensions import Required

from numpy import char
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
from falsk_cors import CORS
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
user_post_args.add_argument("serverID", type=int, required=True)
user_post_args.add_argument("ID", type=int, required=True)
user_post_args.add_argument("characters", action='append')
user_post_args.add_argument("muted", type=int)
user_post_args.add_argument("warnings", type=int)
user_post_args.add_argument("exp", type=int)
user_post_args.add_argument("birthdate", type=str)

#request parser for a PUT request on the user list :
user_put_args = reqparse.RequestParser()
user_put_args.add_argument("serverID", type=int)
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
stats_put_args = reqparse.RequestPArser()
stats_put_args.add_argument("ID", type=int)
stats_put_args.add_argument("name", type=str)
stats_put_args.add_argument("value", type=int)

#We create a list of stats and add the content of the ./DATA/STATS.json to it.
with open("./DATA/STATS.json", "r") as rf:
	stats = json.load(rf)