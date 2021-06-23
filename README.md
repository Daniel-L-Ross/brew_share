# brew_share API

## Setup

1. Clone this repository and change to the directory in the terminal.
1. Run `pipenv shell`
1. Run `pipenv install`
1. Type this exact thing into the terminal to run the migrations and seed the database: `./seed.sh`. You may need to run `chmod +x seed.sh` to make the seed file executable.

Now that your database is set up all you have to do is run the command:

```sh
python manage.py runserver
```

## brew_share ERD

Open the [brew_share database diagram](https://dbdiagram.io/d/60d3569fdd6a5971481c4fb4) in the browser to view the tables and relationships for your database.

## Postman Request Collection

1. Open Postman
1. Click Import from the navbar
1. Choose the Link option
1. Paste in this URL:
    `https://www.getpostman.com/collections/5b8577b6e333dab7ead4`
1. Your should be prompted to import **brew_share API**.
1. Click the Import button to complete the process.

To test it out, expand the brewer profile sub-collection, double-click on Get single user detail and send the request. You should get a response back that looks like this.

```json
{
    "user": {
        "first_name": "Dan",
        "last_name": "Ross",
        "username": "notdanross"
    },
    "bio": "holder of knowledge",
    "profile_image": "http://localhost:8000/media/user_pics/2021/06/10/dan_suit_copy.png",
    "current_coffee": "Humphrey's Street Adado",
    "current_brew_method": "Pour over"
}
```

## Client
The react client for this app can be cloned here [brew_share_client](https://github.com/Daniel-L-Ross/brew_share_client).
## Acknowledgements

Special thanks to my project manager [Jayna Leitze](https://github.com/JaynaLeitze) for her guidance and encouragement to help get this project completed on time.  

## License
Open Source project. 
