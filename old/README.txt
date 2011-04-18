Description
-----------

The Daily Edition is created anew each morning. It contains a number
of articles from a variety of RSS feeds.

Prerequistes
------------

* Python 2.5 or greater.

* If you have Python 2.5, you'll need the simplejson module.

* Python's feedparser module.

Quick Start
-----------

(1) Create a file called 'authors.txt' which contains the full
    name of an author on each line. The authors should be listed
    in order of importance to the reader. Each author should
    have an entry on whoisi.com.

(2) Run 'python publish_edition.py -w'.

(3) Open daily-edition.html in a web browser.

Additional Notes
----------------

NOTE: Not all of this is implemented!

Each issue can only contain a maximum number of articles, as
specified by the reader. Optionally, the reader may also specify
a maximum number of articles by the same author, to ensure
diversity of sources.

The RSS feeds drawn from each issue are found by querying whoisi.com
for the names of various individuals called "influencers", which are
an ordered list provided by the reader.  The list is ordered from
"most influential" to "least influential".

The program creating each issue is "aware" of what previous issues
have contained, so as to ensure that no two issues have the same
article.

Whether an influencer's article is included in an issue should take
into account:

 * Influence
   the author's rank, from 0 (highest) to [of authors] (lowest).
   (lower -> higher likelihood of inclusion)

 * Recency
   time passed since the article was first written.
   (more recent -> higher likelihood of inclusion)

 * Diversity
   time passed since the author was last featured in an issue.
   (less recent -> higher likelihood of inclusion)

data stores:

* a collection of AUTHORS, each AUTHOR has a NAME and RANK. The
  NAME is a unique identifier.

* a collection of ARTICLES, each ARTICLE has an AUTHOR, TITLE, DATE,
  CONTENT, and URL.  The URL is a unique identifier.

* a collection of ISSUES, each ISSUE has a NUMBER, DATE and a list
  of ARTICLES. The NUMBER is a unique identifier.
