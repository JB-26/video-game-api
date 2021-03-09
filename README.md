## Video Game API

Welcome to the Video Game API! A free to use API that I created as a side project so I can practice Python and Flask. This API is publicly available and is hosted on Heroku. The project has it's own page (built with Flask), located here.

Feel free to clone this repo if you want to take a look at how this works!

The database has been populated with some games.

This might not be the best looking website in the world, but it's functional!

## What can I do?

You can....

* Add a game to the database
* Retrieve an individual game from the database
* Get all games in the database
* Delete a game from the database

This API uses JWT so you will need to authenticate yourself.

## Adding a game

To add a game, you will need to access the 'addGame' endpoint (using a POST method) with a request in the following JSON structure:
```
{
    "name": "Super Mario 64",
    "platform": "Nintendo 64",
    "publisher": "Nintendo",
    "genre": "Platformer",
    "year": 1996
}
```

## Deleting a game
To delete a game, you will need to access the 'game' endpoint (using a DELETE method) with the ID of the game you wish to delete. Example:
```
http://127.0.0.1:5000/game/2
```

## Getting a game
To find a specific game, you will need to access the 'game' endpoint (using a GET method) with the ID of the game you wish to find. Example:
```
http://127.0.0.1:5000/game/2
```

## Displaying all games

## Tech Stack
The following was used for this application:

**Backend**
* Python
    * [Flask framework](https://flask.palletsprojects.com/en/1.1.x/)
    * [Flask JWT Extended](https://pypi.org/project/Flask-JWT-Extended/)
    * Flask Restful
    * SQL Alchemy
    * os

**Frontend**
* Bootstrap
    * Uses jsDelivr CDN to include the compiled CSS and JS

