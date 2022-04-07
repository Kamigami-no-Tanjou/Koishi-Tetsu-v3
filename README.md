# Koishi Tetsu v3
The goal of this bot is to take care of all the basic moderation tasks, as well as a few specific functions that are mostly issued from my desires.

The creation will be done in three different steps.
- An API
- The discord part
- A web-application to set the parameters

## API
The API will be RESTful and made with Python, using the Flask Restful library. It'll allow the bot to store and retrieve real time data in a JSON format, easy to parse and to save. Some data might have to be encrypted, to make sure to respect users' privacy.

## Discord part
The discord part will simply be acting just like a random bot. It'll answer commands from the users, triggered by specific messages or reactions. The main objective is to provide at least the same amount of functions and quality as its predecessor.

## Web-Application
I'm quite yet to decide how I will realize it exactly, though I know I will have to implement an authentification system. The safest way to make it would be to use discord's one, but I have no idea how they make it work. <br>
Once connected, it will allow the user to see and modify the parameters of a specific server.