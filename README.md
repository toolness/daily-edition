# The Daily Edition: Information in Moderation

Today's news aggregators take a super-sized approach to feeding you with
information: there's so much awesome in the world that it's hard to keep up
with it without feeling like you *have* to keep up with it. They also make it
easy to spend so much time keeping up with awesome that you're not left with
any time to make your own.

The Daily Edition is a simple website that aims to keep you informed about
what your friends and colleagues are writing about without overwhelming you or
eating up all your time.

Let's make an analogy: words are like calories. The Daily Edition aims to
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

You'll need git and Python 2.5 or above. The few remaining dependencies are
installed for you in a virtual environment.

At your shell prompt, run:

    $ git clone https://toolness@github.com/toolness/daily-edition.git
    $ cd daily-edition
    $ python manage.py bootstrap
    $ python manage.py syncdb
    $ python manage.py loaddata people
    $ python manage.py runserver

During this process, you'll be asked if you want to create a new superuser. Do
so, and remember the username and password.

Once you're done, open your web browser to http://127.0.0.1:8000/ to start
using the app.

## Deployment

This website is a Django app. If you want to run it on a production server,
you'll probably want to run `setup.py install` and either add the app to an
existing Django site or use the sample one in the `dev` directory as a basis
for a new site. See `dev/settings.py` for information on specific settings
that the app uses, and run `manage.py test daily_edition` to make sure that
the app integrates properly with your setup.
