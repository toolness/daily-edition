class IArticle(object):
    """
    Represents an article written by someone; usually a blog post.
    """

    @property
    def url(self):
        """
        The URL for the article, as a Unicode string.
        """

        raise NotImplementedError()

    @property
    def title(self):
        """
        The article's title, as a Unicode string.
        """

        raise NotImplementedError()

    @property
    def content(self):
        """
        The article's content, as a Unicode HTML string.
        """

        raise NotImplementedError()

    @property
    def pub_date(self):
        """
        The article's publication date, as a datetime.datetime object.
        """

        raise NotImplementedError()

    @property
    def author(self):
        """
        The article's author; an object that exposes an IAuthor
        interface.
        """

        raise NotImplementedError()

class IAuthor(object):
    """
    Represents someone who writes articles.
    """

    @property
    def name(self):
        """
        The author's full name, as a Unicode string.
        """

        raise NotImplementedError()

    @property
    def aliases(self):
        """
        The author's aliases; a tuple of Unicode strings.
        """

        raise NotImplementedError()

class IArticleRepository(object):
    """
    Represents a library of articles.
    """

    def get_articles(self, author, start_date, end_date):
        """
        Return a tuple of IArticle objects by the given IAuthor that
        were published between the given datetime.datetime dates
        (inclusive).
        """

        raise NotImplementedError()

class IIssue(object):
    """
    Represents an issue, or edition, that captures a number of
    articles published between two dates (inclusive).
    """

    def articles(self):
        """
        Return a tuple of IArticle objects representing the
        articles in the issue.
        """

        raise NotImplementedError()

    def start_date(self):
        """
        A datetime.datetime object representing the starting date
        of the period that this issue encapsulates.
        """

        raise NotImplementedError()

    def pub_date(self):
        """
        A datetime.datetime object representing the publication
        date of the issue, as well as the end date of the period
        that this issue encapsulates.
        """

        raise NotImplementedError()
