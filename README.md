Public People
=============

This django app provides a basic user interface showing news and public
post/membership history about public people. It also provides an API for
retrieving the identity and post data about persons, and an interface for
administrators to manage the person data.

Person data is in the [Popolo standard](http://www.popoloproject.com/).
We get our baseline data from [Peoples' Assembly](https://pa.org.za/help/api),
but we can correct it directly in this database.

How this project is organised
-----------------------------

On the server:

* uses [dj-database-url](https://crate.io/packages/dj-database-url/) for database URL injection
* uses [django-pipeline](https://django-pipeline.readthedocs.org/en/latest/) for asset compilation and fingerprinting
* uses [pyscss](http://pyscss.readthedocs.org/en/latest/) for compiling SCSS to CSS
* Bower to install assets
* better debugging with ``python manage.py runserver_plus`` from [django-extensions](http://django-extensions.readthedocs.org/en/latest/)
* cookies for session storage

On the client:

* JQuery
* Google Analytics
* Bootstrap
* FontAwesome

Setting up your dev environment
-------------------------------

Configuration for running the server and database in docker-compose has been provided. The simplest way to get up and running is using docker-compose but nothin strictly depends on it, so feel free to set up another way, bearing in mind that less support would be available.

The following only has to be run the first time you set up your development environment, or when you've deleted the database volume and want to set it up again.

1. Clone this git repository and change into the repository directory.

2. Start and create the database - this will keep the docker-compose log running in this shell

```
docker-compose up db
```

3. Then in another shell prompt, initialise the database and superuser:

```
docker-compose run --rm web python manage.py migrate
docker-compose run --rm web python manage.py createsuperuser
```

4. Start the sample data server

```
docker-compose -f docker-compose.yml -f docker-compose.dev-data.yml up -d dev-data
```

5. Load some example popolo data:

```
docker-compose run --rm web python manage.py popolo_sources_update --create http://dev-data:8001/pombola.json
```

Then you can run the server

```
docker-compose up -d web
```

You can log in as your new superuser and explore the data using the admin interface at http://localhost:8000/admin and the public interface at http://localhost:8000/

Search for one of the names in the example popolo data to see the site working.


Subsequently, you only need to start the database and server with

```
docker-compose up
```


Development
-----------

* Put javascript into ``code4sa/static/javascript/app.js``
* Put SCSS stylesheets into ``code4sa/static/stylesheets/app.scss``
* Install new asset packs with Bower: ``bower install -Sp package-to-install``
* Get better debugging with ``python manage.py runserver_plus``

Production deployment
---------------------

Production deployment is based on running the app on dokku

### Intitial deployment

```bash
dokku apps:create publicpeople
dokku config:set DATABASE_URL=postgresql://.../publicpeople \
                 DJANGO_DEBUG=false \
                 DISABLE_COLLECTSTATIC=1 \
                 DJANGO_SECRET_KEY=some-secret-key \
                 NEW_RELIC_APP_NAME=cool app name \
                 NEW_RELIC_LICENSE_KEY=new relic license key
```

After pushing to the dokku git remote:

```
dokku run publicpeople python manage.py migrate
dokku run publicpeople python manage.py createsuperuser
```

### Regular change deployment

```
git push dokku master
```

Updating popolo data
--------------------

The first time, create the source

```
dokku run publicpeople python app/manage.py popolo_sources_update --create https://www.pa.org.za/media_root/popolo_json/pombola.json
```

Subsequently, just update (without `--create`)

```
dokku run publicpeople python app/manage.py popolo_sources_update https://www.pa.org.za/media_root/popolo_json/pombola.json
```

Accessing the data
------------------

### People API

The People API can be explored interactively at https://publicpeople.org.za/api/

### News API

[An example query to the News API](https://alephapi.public-people.techforgood.org.za/api/2/search?q=%22ace+magashule%22&sort=published_at)

[News API documentation](https://github.com/alephdata/aleph/wiki/API)

License
-------

MIT License

Attribution
-----------

- Repo structure based on https://github.com/openupsa/django-template
- REST API based on https://github.com/openpolis/popolorest/blob/master/popolorest/views.py
