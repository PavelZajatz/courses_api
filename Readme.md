# REST API With Flask & SQL Alchemy(SQLite)

> Course API using Python Flask, SQL Alchemy and Marshmallow

## Quick Start

``` bash

# Install dependencies
$ pip install -r requirements.txt

# Create DB
$ python
>> from app import db
>> db.create_all()
>> exit()

# Run Server (http://localhst:5000)
python app.py
```

## Endpoints

* GET     /course
* GET     /course/:id
* POST    /course
* PUT     /course/:id
* DELETE  /course/:id

## Tests
``` bash
# Run tests
pytest
```