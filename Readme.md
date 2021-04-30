# REST API With Flask & SQL Alchemy(SQLite)

> Course API using Python Flask, SQL Alchemy and Marshmallow

## Quick Start

``` bash

# Install dependencies:
$ pip install -r requirements.txt

# Create DB;
$ python
>> from app import db
>> db.create_all()
>> exit()

# Run Server (http://localhost:5000):
python app.py
```

## Endpoints

* GET     /course
* GET     /course/:id
* POST    /course
* PUT     /course/:id
* DELETE  /course/:id


## Examples of requests
``` bash
# Create a new course:
curl --location --request POST 'http://localhost:5000/course' \
--header 'Content-Type: application/json' \
--data-raw '{
    "title": "Python for beginners",
    "start_date": 1622103552000,
    "finish_date": 1627373952000,
    "qty": 30
}'

# Get all courses:
curl --location --request GET 'http://localhost:5000/course'

# Get course by id:
curl --location --request GET 'http://localhost:5000/course/1'

# Find a course by title:
curl --location --request GET 'http://localhost:5000/course?searchString=python'

# Filter courses by start day
curl --location --request GET 'http://localhost:5000/course?startCourseFrom=1622103552000&  
startCourseTo=1627373952000'

# Filter courses by finish day
curl --location --request GET 'http://localhost:5000/course?finishCourseFrom=1622103552000&  
finishCourseTo=1627373952000'

# Filter courses by start and finish days
curl --location --request GET 'http://localhost:5000/course?startCourseFrom=1622103552000&  
startCourseTo=1627373952000&finishCourseFrom=1622103552000&finishCourseTo=1627373952000'

# Update a course:
curl --location --request PUT 'http://localhost:5000/course/1' \
--header 'Content-Type: application/json' \
--data-raw '{
    "title": "Python for beginners edited",
    "start_date": 1622103552000,
    "finish_date": 1627373952000,
    "qty": 30
}'

# Delete a course
curl --location --request DELETE 'http://localhost:5000/course/1'

```

## Tests
``` bash
# Run tests:
pytest
```