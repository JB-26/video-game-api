## Video Game API

Welcome to the Video Game API! A free to use RESTful API that I created as a side project so I can practice Python and Flask. This API is publicly available and is hosted on Heroku. The project has it's own page (built with Flask), located [here](https://mighty-cliffs-81365.herokuapp.com/).

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

To add a game to the database, you will need to use the <strong>/addGame</strong> endpoint and submit a POST request. Example:
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
To delete a game from the database, you will need to use the <strong>/deleteGame</strong> endpoint and submit a DELETE request. Example:
```
{
    "id": 3
}
```

## Getting a game
To find a game (or games), you will need to use the <strong>/findGame</strong> endpoint and submit a GET request. Example:
```
{
    "name": "64"
}
```

## Displaying all games
To display all games in the database, you will need to use the <strong>/displayGames</strong> endpoint. Submit a GET request to this endpoint and you will see a list of all the games in the database. Example response:
```
{
    "Games": [
        {
            "Game": {
                "Genre: ": "Fighting",
                "ID: ": 1,
                "Name: ": "X-Men Vs Street Fighter",
                "Platform: ": "Sega Saturn",
                "Publisher: ": "Capcom",
                "Year": 1997
            }
        },
        {
            "Game": {
                "Genre: ": "Platformer",
                "ID: ": 2,
                "Name: ": "Super Mario 64",
                "Platform: ": "Nintendo 64",
                "Publisher: ": "Nintendo",
                "Year": 1996
            }
        },
        {
            "Game": {
                "Genre: ": "Racing",
                "ID: ": 3,
                "Name: ": "Wave Race 64",
                "Platform: ": "Nintendo 64",
                "Publisher: ": "Nintendo",
                "Year": 1996
            }
        }
    ]
}
```

## Updating a game
To update a game in the database, you will need to use the <strong>/updateGame</strong> endpoint and submit a PUT request. Example:
```
{
    "id": 10,
    "field": "name",
    "value": "Wave Race: Blue Storm"
}
```

The field parameter will accept one of the following:

* name
* platform
* publisher
* genre
* year

## Finding a game
To find a game (or games), you will need to use the <strong>/findGame</strong> endpoint and submit a GET request.

The endpoint accepts JSON in the following structure:

{ "name": "64" }

## Tech Stack
The following was used for this application:

**Backend**
* Python
    * [Flask framework](https://flask.palletsprojects.com/en/1.1.x/)
    * [Flask JWT Extended](https://pypi.org/project/Flask-JWT-Extended/)
    * Flask Restful
    * [Flask SQL Alchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/#)
    * os

**Frontend**
* Bootstrap
    * Uses jsDelivr CDN to include the compiled CSS and JS

