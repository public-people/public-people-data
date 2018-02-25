Code4SA Django App Template
===========================

This is Code for South Africa's application template for Django apps.

About this template
-------------------

This template makes it easy to build Django apps that fit the Code for South Africa best practices and guidelines.

On the server:
* easy to deploy on Heroku or Dokku
* uses [dj-database-url](https://crate.io/packages/dj-database-url/) for database URL injection
* uses [django-pipeline](https://django-pipeline.readthedocs.org/en/latest/) for asset compilation and fingerprinting
* uses [pyscss](http://pyscss.readthedocs.org/en/latest/) for compiling SCSS to CSS
* New Relic for monitoring
* Bower to install assets
* better debugging with ``python manage.py runserver_plus`` from [django-extensions](http://django-extensions.readthedocs.org/en/latest/)
* sane logging to stdout
* cookies for session storage

On the client:
* Code for South Africa app templates and layouts
* JQuery
* Google Analytics
* Bootstrap
* FontAwesome

Setting up the template
-----------------------

Create a new repository on Github. Everywhere you see ``$NEW_PROJECT_NAME`` in the following script, replace it with the name of the repository you just created.

```
git clone git@github.com:code4sa/django-template.git $NEW_PROJECT_NAME
cd $NEW_PROJECT_NAME

virtualenv --no-site-packages env
source env/bin/activate
pip install -r requirements.txt
```

Edit ``code4sa/settings.py`` and set some options

* ``GOOGLE_ANALYTICS_ID`` to the GA tracking code

Finally, setup the database:

```
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Using the template
------------------

* Put javascript into ``code4sa/static/javascript/app.js``
* Put SCSS stylesheets into ``code4sa/static/stylesheets/app.scss``
* Install new asset packs with Bower: ``bower install -Sp package-to-install``
* Get better debugging with ``python manage.py runserver_plus``

Production deployment
---------------------

Production deployment assumes you're running on Heroku.

You will need:

* a django secret key
* a New Relic license key
* a cool app name

```bash
heroku create
heroku addons:add heroku-postgresql
heroku config:set DJANGO_DEBUG=false \
                  DISABLE_COLLECTSTATIC=1 \
                  DJANGO_SECRET_KEY=some-secret-key \
                  NEW_RELIC_APP_NAME=cool app name \
                  NEW_RELIC_LICENSE_KEY=new relic license key
git push heroku master
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

License
-------

MIT License
