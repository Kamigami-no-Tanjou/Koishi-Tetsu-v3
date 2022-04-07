from typing_extensions import Required
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