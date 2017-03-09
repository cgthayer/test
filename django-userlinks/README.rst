=========
UserLinks
=========

This makes it easy to like, and bookmark arbitrary things in your
system. It links a user to to any "object", with a link-type, where an
object is a type (ContentType / table / Model) and an ID (object_id,
or primary key column).  For example "User A 'liked' Spot 20", "User C
'bookmarked' Article 'I love django'", "User C 'is-friends-with' User
A".

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "userlinks" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'userlinks',
    ]

2. Include the userlinks URLconf in your project urls.py like this::

    url(r'^userlinks/', include('userlinks.urls')),

3. Run `python manage.py migrate` to create the UserLink models.

4. Run `python manage.py collectstatic` to get the static parts.

5. Run `python manage.py runserver` to verify it's starting.


Testing it out
-----------

1. `cd /tmp; django-admin startproject stubproj; cd stubproj`

2. Copy over the files `cp -r ../userlinks .`

3. Add "userlinks" to your INSTALLED_APPS stubproj/settings.py like this::

    INSTALLED_APPS = [
        ...
        'userlinks',
    ]

4. Include regular urls and the eg_urls like this in your stubproj/urls.py::

    url(r'^userlinks/', include('userlinks.urls')),
    url(r'^userlinks/', include('userlinks.eg_urls')),

5. You'll want jquery, fontawesome, and animateCss, but we've throw in enough for testing.

6. Run `python manage.py migrate`

7. Run `python manage.py collectstatic`

8. Run `python manage.py runserver`

9. Point your browser at http://localhost:8000/userlinks_eg/


