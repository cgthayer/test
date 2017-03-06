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

2. Include the polls URLconf in your project urls.py like this::

    url(r'^userlinks/', include('userlinks.urls')),

3. Run `python manage.py migrate` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a userlink (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/userlinks/ to play around.

