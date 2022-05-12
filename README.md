[JDA-shield]: https://img.shields.io/badge/Discord%20API-JDA-blue.svg
[flask-shield]: https://img.shields.io/badge/Framework-Flask-purple.svg
[license-shield]: https://img.shields.io/badge/License-MIT-white.svg
[discord-shield]: https://discord.com/api/guilds/861918152669396992/widget.png

[JDA]: https://github.com/DV8FromTheWorld/JDA
[flask]: https://flask.palletsprojects.com/en/2.1.x/
[license]: https://github.com/Kamigami-no-Tanjou/Koishi-Tetsu-v3/blob/main/LICENSE
[discord]: https://discord.gg/g6XuGQTKZd

[ ![flask-shield][] ][flask]
[ ![JDA-shield][] ][JDA]

[ ![license-shield][] ][license]
[ ![discord-shield][] ][discord]

# Koishi Tetsu v3
The goal of this bot is to take care of all the basic moderation tasks, as well as a few specific functions that are mostly issued from my desires.

The creation will be done in three different steps.
- An API
- The discord part
- A web-application to set the parameters

## API
The API will be RESTful and made with Python, using the Flask Restful library. It'll allow the bot to store and retrieve real time data in a JSON format, easy to parse and to save. Some data might have to be encrypted, to make sure to respect users' privacy.

### API Dependencies :
Here I will list all the python modules you'll have to install to make the API run correctly.
- flask
- flask_restful
- flask_cors

## Discord part
The discord part will simply be acting just like a random bot. It'll answer commands from the users, triggered by specific messages or reactions. The main objective is to provide at least the same amount of functions and quality as its predecessor.

## Web-Application
I'm quite yet to decide how I will realize it exactly, though I know I will have to implement an authentification system. The safest way to make it would be to use discord's one, but I have no idea how they make it work. <br>
Once connected, it will allow the user to see and modify the parameters of a specific server.

## Legal terms
As every project available to public in this organization, it is licensed under MIT copyright. More info by clicking the License shield at the top.