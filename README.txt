
A simple example of a restful web service

Simon: This README is written pretty much with you exclusively in mind.


Dependencies
------------

  * Tested on Windows XP
  * Python 2.7

Product code requires the Python packages:

  * web.py 0.34

For development & running tests, also requires the Python packages:

  * nose 1.0.0
  * mock 0.7.0


Usage
-----

Start the server with::

    python run-server.py

This starts listening on localhost:8080


Tests
-----

Try either of::

    make tests

or::

    nosetests .

Running tests using 'python -m unittest' will not work, since this does not
play nicely with relative imports in the product code, which I do use.

Unit tests have very limited coverage. The single acceptance test exercises all
API entry points, but does not attempt to stimulate any error conditions.

All tests currently pass.


Design
------

Spec requires that we provide::

    add_category(category, parent)
    get_subcategories(category)
    get_lineage(category)

I diverged from the spec in two main ways that I'm aware of. Firstly,
I added a new entry point::

    get_category(category)

Secondly, I didn't like the use of category names as identifiers, because it
prevents two subcategories from sharing the same name, so I switched out
occurences of category names with a UID::

    add_category(category_name, parent_id)
    get_subcategories(category_id)
    get_lineage(category_id)
    get_category(category_id)


These functions are implemented in api.py



Resources
---------

Decided on two types of resources, with the following JSON representations:

category::

    {
        name="NAME",
        uri="CAT_URI",
        parent="CAT_URI",
        children="CHILD_URI",
        lineage="LINEAGE_URI",
    }

category_list::

    [
        {
            name="NAME",
            uri="CAT_URI",
        },
        ...
    ]


The JSON encoding of representations is what is returned by the specced
API functions, and is put into the HTTP responses.

These structures are created by the functions in representation.py

 
URIs
----

I expose the specced functions through the following URIs:

GET  /children/ID   get_subcategories(cat_id=None)
                    With no ID gets top-level categories
                    Returns a category_list

POST /children/ID   add_category(cat_id=None)
name=NAME           With no ID, creates new top-level category
                    Returns a category

GET  /category/ID   get_category(cat_id)
                    Returns a category

GET  /lineage/ID    get_lineage(cat_id)
                    Returns a category


In addition the root URI / is an alias for /children, so that:

GET /   returns a list of top-level categories

POST /  creates & returns a new top-level category


These URIs are mapped to handlers in the file server.py.


Known Issues
------------

Embarassingly many. I was running short of time and had problems getting up
to speed with my chosen framework (web.py), so I ended up cutting a lot of
corners:

I don't even have a persistant back-end. I whipped up a simple dictionary
to act as storage while I got started, and ran out of time before replacing it.

I pay no attention to content-types.

I don't even try to return the right HTTP status codes for bad requests.

Test coverage is very limited. The single acceptance test runs through a
sunny-day scenario that does exercise all of the API entry points, but it
doesn't really stress them, nor does it attempt to stimulate any errors.
Unit tests only cover part of the 'server' module, and don't cover any error
conditions.


Thoughts
--------

In a real project, I'd pro-actively communicate a lot more, to uncover and
resolve ambiguities and misunderstandings. For this quiz though, I figured that
any gaps in my understanding of the spec were part of the exercise, so instead
used my own judgement to fill them in.



Thanks
------

Big ups to Christian Muirhead for an invaluable chat to review my approach.


Contact
-------

Written by Jonathan Hartley, tartley at tartley dot com, 07737 062 225

