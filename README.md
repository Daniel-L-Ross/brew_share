# brew_share API

## Prerequisites

### Mac OS

```sh
brew install libtiff libjpeg webp little-cms2
```

## Setup

1. Clone this repository and change to the directory in the terminal.
1. Run `pipenv shell`
1. Run `pipenv install`
1. Type this exact thing into the terminal to run the migrations and seed the database: `./seed_data.sh`

Now that your database is set up all you have to do is run the command:

```sh
python manage.py runserver
```

## Bangazon ERD

Open the [brew_share database diagram](https://dbdiagram.io/d/60d3569fdd6a5971481c4fb4) in the browser to view the tables and relationships for your database.

## Postman Request Collection

1. Open Postman
1. Click Import from the navbar
1. Choose the Link option
1. Paste in this URL:
    `https://www.getpostman.com/collections/5b8577b6e333dab7ead4`
1. Your should be prompted to import **brew_share API**.
1. Click the Import button to complete the process.

To test it out, expand the Profile sub-collection, double-click on Login and send the request. You should get a response back that looks like this.

```json
{
    "valid": true,
    "token": "9ba45f09651c5b0c404f37a2d2572c026c146690",
    "id": 5
}
```

## Documentation

To view browser-based documentation for the project, follow these steps.

1. Run `./renderdocs.sh`
1. `cd docs`
1. Then start a simple web server like `http-server` or `serve`.
1. In your web browser, go to the URL provided by your web server.

![documentation site](./bangazon-docs.png)