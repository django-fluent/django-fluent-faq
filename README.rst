django-fluent-faq
=================

This Django application adds a FAQ engine to sites built with django-fluent_ CMS.

Features:

* Multilingual
* Multisite
* Categories and questions
* SEO fields (meta keywords, description)

Used applications:

* Multilingual support based on django-parler_.
* *Optional* integration with django-taggit_ and django-taggit-autocomplete-modified_ for tag support
* *Optional* integration with django-fluent-pages_
* *Optional* integration with django.contrib.sitemaps_


Installation
============

First install the module, preferably in a virtual environment:

.. code-block:: bash

    git clone https://github.com/edoburu/django-fluent-faq.git
    cd django-fluent-faq
    pip install .

    # Install the plugins of fluent-contents that you use:
    pip install django-fluent-contents[text]

    # Optional: to add tagging support + autocomplete use:
    pip install django-taggit django-taggit-autocomplete-modified


Configuration
-------------

Add the applications to ``settings.py``:

.. code-block:: python

    INSTALLED_APPS += (
        # FAQ engine
        'fluent_faq',

        # The content plugins
        'fluent_contents',
        'fluent_contents.plugins.text',

        # Support libs
        'categories',
        'categories.editor',
        'django_wysiwyg',

        # Optional tagging
        'taggit',
        'taggit_autocomplete_modified',
    )

    DJANGO_WYSIWYG_FLAVOR = "yui_advanced"

Note that not all applications are required;
tagging is optional, and so are the various ``fluent_contents.plugin.*`` packages.

Include the apps in ``urls.py``:

.. code-block:: python

    urlpatterns += patterns('',
        url(r'^admin/util/taggit_autocomplete_modified/', include('taggit_autocomplete_modified.urls')),
        url(r'^faq/', include('fluent_faq.urls')),
    )

The database can be created afterwards:

.. code-block:: bash

    ./manage.py syncdb

In case additional plugins of django-fluent-contents_ are used, follow their
`installation instructions <https://django-fluent-contents.readthedocs.io/en/latest/plugins/index.html>`_ as well.
Typically this includes:

* adding the package name to ``INSTALLED_APPS``.
* running ``pip install django-fluent-contents[pluginname]``
* running  ``./manage.py syncdb``


Configuring allowed plugins
---------------------------

To limit which plugins for django-fluent-contents_ can be used in the FAQ answer, use:

.. code-block:: python

    FLUENT_CONTENTS_PLACEHOLDER_CONFIG = {
        'faq_answer': {
            'plugins': (
                'TextPlugin', 'PicturePlugin', 'OEmbedPlugin', 'SharedContentPlugin', 'RawHtmlPlugin',
            ),
        },
    }


Configuring the templates
-------------------------

To display the blog contents, a ``fluent_faq/base.html`` file needs to be created.
This will be used to map the output of the module to your site templates.

The base template needs to have the blocks:

* ``content`` - displays the main content
* ``sidebar_content`` - displays the sidebar content
* ``title`` - the title fragment to insert to the ``<title>`` tag.
* ``meta-title`` - the full contents of the ``<title>`` tag.
* ``meta-description`` - the ``value`` of the meta-description tag.
* ``meta-keywords`` - the ``value`` for the meta-keywords tag.
* ``og-type`` - the OpenGraph type for Facebook (optional)
* ``og-description`` the OpenGraph description for Facebook (optional)

The ``fluent_faq/base.html`` template could simply remap the block names to the site's ``base.html`` template.
For example:

.. code-block:: html+django

    {% extends "base.html" %}

    {% block headtitle %}{% block title %}{% endblock %}{% endblock %}

    {% block main %}
        {# This area is filled with the question details:
        {% block content %}{% endblock %}

        {# Add any common layout, e.g. a sidebar here #}
        {% block sidebar_content %}{% endblock %}
    {% endblock %}

When all other block names are already available in the site's ``base.html`` template,
this example should be sufficient.


Adding pages to the sitemap
---------------------------

Optionally, the blog pages can be included in the sitemap.
Add the following in ``urls.py``:

.. code-block:: python

    from fluent_faq.sitemaps import FaqQuestionSitemap, FaqCategorySitemap

    sitemaps = {
        'faq_questions': FaqQuestionSitemap,
        'faq_categories': FaqCategorySitemap,
    }

    urlpatterns += patterns('',
        url(r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    )


Integration with django-fluent-pages:
-------------------------------------

To integrate with the page types of django-fluent-pages_, don't include ``fluent_blogs.urls`` in the URLconf:

.. code-block:: python

    urlpatterns += patterns('',
        url(r'^admin/util/taggit_autocomplete_modified/', include('taggit_autocomplete_modified.urls')),
    )

Instead, add a page type instead:

.. code-block:: python

    INSTALLED_APPS += (
        'fluent_pages',
        'fluent_faq.pagetypes.faqpage',
    )

A "FAQ Module" page can now be created in the page tree of django-fluent-pages_
at the desired URL path.


Contributing
------------

This module is designed to be generic, and easy to plug into your site.
In case there is anything you didn't like about it, or think it's not
flexible enough, please let us know. We'd love to improve it!

If you have any other valuable contribution, suggestion or idea,
please let us know as well because we will look into it.
Pull requests are welcome too. :-)



.. _django-fluent: http://django-fluent.org/
.. _django.contrib.sitemaps: https://docs.djangoproject.com/en/dev/ref/contrib/sitemaps/
.. _django-fluent-contents: https://github.com/edoburu/django-fluent-contents
.. _django-fluent-pages: https://github.com/edoburu/django-fluent-pages
.. _django-parler: https://github.com/edoburu/django-parler
.. _django-taggit: https://github.com/alex/django-taggit
.. _django-taggit-autocomplete-modified: http://packages.python.org/django-taggit-autocomplete-modified/
