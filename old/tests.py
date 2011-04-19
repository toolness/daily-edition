import os
import tempfile
import urllib2
import StringIO
import datetime
from distutils.dir_util import remove_tree

from django.test import TestCase
from django.utils import feedgenerator
from daily_edition.tests import install_sample_data
from daily_edition.models import Person
import publish_edition

class FakeResponse(StringIO.StringIO):
    def info(self):
        return {}

class FakeDateTime(object):
    def __init__(self, now):
        self._now = now
        
    def now(self):
        return self._now
    
class FakeDate(object):
    def __init__(self, today):
        self._today = today

    def __call__(self, *args, **kwargs):
        return datetime.date(*args, **kwargs)
        
    def today(self):
        return self._today
        
class LegacyTests(TestCase):
    def setUp(self):
        install_sample_data()
        self.dir = tempfile.mkdtemp('.daily_edition')
        self.cache_dir = os.path.join(self.dir, 'cache')
        self.output_dir = os.path.join(self.dir, 'editions')
        self.authors_filename = os.path.join(self.dir, 'authors.txt')
        self.stdout = StringIO.StringIO()
        self.old_stdout = publish_edition.stdout
        self.old_urlopen = urllib2.urlopen
        self.old_date = publish_edition.date
        self.old_datetime = publish_edition.datetime
        publish_edition.date = FakeDate(datetime.date(2010, 1, 1))
        publish_edition.datetime = FakeDateTime(datetime.datetime(2010, 1, 1))
        urllib2.urlopen = self.fake_urlopen
        publish_edition.set_stdout(self.stdout)
        os.mkdir(self.cache_dir)
        os.mkdir(self.output_dir)
        open(self.authors_filename, 'w').close()

    def tearDown(self):
        urllib2.urlopen = self.old_urlopen
        publish_edition.date = self.old_date
        publish_edition.datetime = self.old_datetime
        publish_edition.set_stdout(self.old_stdout)
        remove_tree(self.dir)

    def set_authors(self, *names):
        open(self.authors_filename, 'w').write('\n'.join(names))

    def fake_urlopen(self, request):
        url = request.get_full_url()
        f = feedgenerator.Atom1Feed(
            title=u"My Weblog",
            link=u"http://www.example.com/",
            description=u"In which I write about what I ate today.",
            language=u"en",
            author_name=u"Myself",
            feed_url=u"http://example.com/atom.xml"
            )
        if url == 'http://chrisblizzard.blip.tv/rss':
            title = u"Blizzard blip.tv Post"
        elif url == 'http://www.0xdeadbeef.com/weblog/?feed=rss2':
            title = u"Blizzard 0xdeadbeef post"
        elif url == 'http://shaver.off.net/diary/feed/atom/':
            title = u"Shaver post"
        else:
            raise Exception('Unexpected URL: %s' % url)
        f.add_item(
            title=title,
            link=u"http://www.example.com/entries/1/",
            pubdate=datetime.datetime.now(),
            description=u"<p>Hello there.</p>"
            )
        return FakeResponse(f.writeString('UTF-8'))

    def publish_edition(self, **kwargs):
        publish_edition.publish_edition(
            people=Person,
            output_dir=self.output_dir,
            cache_dir=self.cache_dir,
            authors_filename=self.authors_filename,
            **kwargs
            )

    def test_publish_edition_works(self):
        self.set_authors('Christopher Blizzard', 'Mike Shaver')
        self.publish_edition(update_urls=True, min_article_word_count=1)
        
        expect = {
            u'articles': {
                u'Christopher Blizzard': [{
                    u'content': [{u'base': u'',
                                  u'language': u'en',
                                  u'type': u'text/html',
                                  u'value': u'<p>Hello there.</p>'}],
                    u'pubDate': [2011, 4, 19],
                    u'title': u'Blizzard blip.tv Post',
                    u'url': u'http://www.example.com/entries/1/'
                    }],
                u'Mike Shaver': [{
                    u'content': [{u'base': u'',
                                  u'language': u'en',
                                  u'type': u'text/html',
                                  u'value': u'<p>Hello there.</p>'}],
                    u'pubDate': [2011, 4, 19],
                    u'title': u'Shaver post',
                    u'url': u'http://www.example.com/entries/1/'
                    }]},
            u'authors': [u'Christopher Blizzard', u'Mike Shaver'],
            u'id': 0,
            u'pubDate': [2010, 1, 1]
            }

        f = open(os.path.join(self.output_dir, 'daily-edition.json'), 'r')
        actual = publish_edition.json.load(f)
        self.assertDictEqual(expect, actual)
