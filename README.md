# The Daily Edition: Information in Moderation

The Daily Edition is a simple website that aims to keep you informed about
what your friends and colleagues are writing about without overwhelming you or
eating up all your time.

To make an analogy: words are like calories. The Daily Edition aims to
prevent information obesity by delivering your news in a series of *issues*
that are constrained by the number of words they can contain. 2500 of them, to
be precise.

You start by telling The Daily Edition who your *influencers* are: these are
the luminaries who inspire you to do awesome things. Specifically, your
influencers are an *ordered list*: the higher a name is on the list, the more
likely it is for an issue to contain news from them.

The Daily Edition values diversity in an information diet, too, though. If one
of your influencers is a prolific blogger who writes 3 posts a day, every
issue will only contain *one* of those posts, to make room for other voices.

Publishing and reading an issue a day is just a recommendation, however.
You're welcome to publish more issues. But every time you finish reading an
issue, you might want to ask yourself if your time is best spent consuming
more awesome, or making your own.

## Quick Start

You'll need git and Python 2.5 or above.

At your shell prompt, run:

    $ git clone --recursive git://github.com/toolness/daily-edition.git
    $ cd daily-edition/de_site
    $ python manage.py syncdb
    $ python manage.py loaddata people
    $ python manage.py runserver

During this process, you'll be asked if you want to create a new superuser. Do
so, and remember the username and password.

Once you're done, open your web browser to http://127.0.0.1:8000/ to start
using the app.

## Deployment

This website is a Django app.

Copy `de_site/settings_local.sample.py` to `de_site/settings_local.py` 
and edit as necessary. Run `manage.py test daily_edition` to make sure that
the app integrates properly with your setup.

See `fabfile.py`, a [Fabric][] script, for more context on what's needed
to deploy the app.

## Limitations

This app was originally implemented in early 2010 as a command-line utility
that used Christopher Blizzard's [whoisi][] as a repository for influencer
identity information. Since then, whoisi.com has been shut down and the
command-line utility has been turned into a multi-user Django app, which means
a few things:

* The back-end implementation doesn't scale well at all. At best, each
  deployment of The Daily Edition can probably only be used to serve a handful
  of people, rather than hundreds or millions.

* Adding or changing information about influencers can only be done via the
  Django admin interface.

  [whoisi]: http://www.0xdeadbeef.com/weblog/2008/06/announcing-whoisi/
  [Fabric]: http://www.fabfile.org
