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

Setting up
----------

[Create a database](https://gist.github.com/jbothma/8a9a30399c2091d89763bff0a1952da4)

Then, the first time you run the server, run migrations and create a superuser

```
python manage.py migrate
python manage.py createsuperuser
```

See [Download and update Popolo data](#updating-popolo-data), running those
commands without the `dokku run publicpeople` part.

Then you can run the server

```
python manage.py runserver
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

[An example query to the News API](https://alephapi.public-people.techforgood.org.za/api/2/search?q="ace magashule"&sort=published_at)

[News API documentation](https://github.com/alephdata/aleph/wiki/API)

License
-------

MIT License

Attribution
-----------

- Repo structure based on https://github.com/openupsa/django-template
- REST API based on https://github.com/openpolis/popolorest/blob/master/popolorest/views.py