# netguru-movies

## TASK
We'd like you to build simple REST API for us - a basic movie database interacting with external API. Here's full specification of endpoints that we'd like it to have:

* POST /movies:
```
​Request body should contain only movie title, and its presence should be validated.
Based on passed title, other movie details should be fetched from http://www.omdbapi.com/ (or other similar, public movie database) - and saved to application database.
Request response should include full movie object, along with all data fetched from external API.
```

* GET /movies:
```
​Should fetch list of all movies already present in application database.
Additional filtering, sorting is fully optional - but some implementation is a bonus.
```
* POST /comments:
```
​Request body should contain ID of movie already present in database, and comment text body.
Comment should be saved to application database and returned in request response.
```
* GET /comments:
```
​Should fetch list of all comments present in application database.
Should allow filtering comments by associated movie, by passing its ID.
```
* GET /top:
```
​Should return top movies already present in the database ranking based on a number of comments added to the movie (as in the example) in the specified date range. The response should include the ID of the movie, position in rank and total number of comments (in the specified date range).
Movies with the same number of comments should have the same position in the ranking.
Should require specifying a date range for which statistics should be generated.
```
* Example response:
```
[
    {
        "movie_id": 2,
        "total_comments": 4,
        "rank": 1
    },
    {
        "movie_id": 3,
        "total_comments": 2,
        "rank": 2
    },
    {
        "movie_id": 4,
        "total_comments": 2,
        "rank": 2
    },
    {
        "movie_id": 1,
        "total_comments": 0,
        "rank": 3
    }

]
```

### Rules & hints​
```
​Your goal is to implement REST API in Django, however you're free to use any third-party libraries and database of your choice, but please share your reasoning behind choosing them.
At least basic tests of endpoints and their functionality are obligatory. Their exact scope and form is left up to you.
The application's code should be kept in a public repository so that we can read it, pull it and build it ourselves. Remember to include README file or at least basic notes on application requirements and setup - we should be able to easily and quickly get it running.
Written application must be hosted and publicly available for us online - we recommend Heroku.
```
### Demo app
An demo app url: `http://macolszewski.pythonanywhere.com` 

## Installation

### Bash

```bash
git clone https://github.com/macolszewski/netguru-movies.git
virtualenv -p python3 yourvirtualenv
source yourvirtualenv/bin/activate
cd net_movies
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### local_settings.py

`settings.py` imports `local_settings.py` (not included to project) which should contains:

* SECRET_KEY -> your django-project sercet key
* ALLOWED_HOSTS -> add your hosts here
* OMDB_API_KEY -> you can obtain key on OMDB site

You can fill `local_settings.template` with your data, and rename file to `local_settings.py`.

### Getting movies:
```
curl -GET http://macolszewski.pythonanywhere.com/movies
```

Optional parameters:
```year: show movies with year equals given value```
```title: show movies with title contains part of given value```

### Getting top movies:
```
curl -GET http://macolszewski.pythonanywhere.com/top
```

### Adding movies:
```
curl -X POST http://macolszewski.pythonanywhere.com/movies -d 'title=movie title'
```

### Removing movies
```
curl -X DELETE http://macolszewski.pythonanywhere.com/movies -d 'title=movie title'
```

### Getting comments:
```
curl -GET http://macolszewski.pythonanywhere.com/comments
```

Optional parameters:
```movie: show comments for given movie id or movie title```

### Adding comments:
```
curl -X POST http://macolszewski.pythonanywhere.com/comments -d 'movie=movie title/movie id&comment_content=comment content'
```

### Removing comments:
```
curl -X DELETE http://macolszewski.pythonanywhere.com/comments -d 'id=comment id'
```
