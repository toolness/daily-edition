import os
import tempfile
import datetime
from distutils.dir_util import remove_tree

from django.test import TestCase
from django.contrib.auth.models import User
import multiuser

class MultiuserTests(TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp('.daily_edition_multiuser')
        self.user = User(username='bob')
        self.mu = multiuser.Account(self.dir, self.user)

    def tearDown(self):
        remove_tree(self.dir)

    def _ensure_dir(self, dirpath, expected_name):
        self.assertEqual(
            dirpath,
            os.path.join(self.dir, 'bob', expected_name)
            )
        self.assertTrue(os.path.exists(dirpath))
        self.assertTrue(os.path.isdir(dirpath))

    def _write_file(self, contents, *parts):
        f = open(os.path.join(*parts), 'w')
        f.write(contents)
        f.close()

    def test_account_makes_root_dir_if_not_exists(self):
        newdir = os.path.join(self.dir, 'nonexistent')
        mu2 = multiuser.Account(newdir, self.user)
        self.assertTrue(os.path.exists(newdir))

    def test_has_issue_returns_false(self):
        self.assertFalse(self.mu.has_issue(), False)
        self.assertFalse(self.mu.has_issue(42), False)

    def test_has_issue_with_latest_issue_returns_true(self):
        self._write_file('[]', self.mu.issues_dir, 'daily-edition.json')
        self.assertTrue(self.mu.has_issue())

    def test_has_issue_with_numbered_issue_returns_true(self):
        self._write_file('[]', self.mu.issues_dir, 'issue-123.json')
        self.assertTrue(self.mu.has_issue(123))

    def test_get_issue_json_with_latest_issue_works(self):
        self._write_file('[5]', self.mu.issues_dir, 'daily-edition.json')
        self.assertEqual(self.mu.get_issue_json(), '[5]')

    def test_get_issue_json_with_numbered_issue_works(self):
        self._write_file('[9]', self.mu.issues_dir, 'issue-526.json')
        self.assertEqual(self.mu.get_issue_json(526), '[9]')

    def test_caches_dir_is_created(self):
        self._ensure_dir(self.mu.caches_dir, 'caches')

    def test_issues_dir_is_created(self):
        self._ensure_dir(self.mu.issues_dir, 'issues')

    def test_authors_dir_is_created(self):
        self._ensure_dir(self.mu.authors_dir, 'authors')

    def test_default_authors_content_is_created(self):
        u = User(username='blop')
        mu = multiuser.Account(self.dir, u, default_authors='hi')
        self.assertEqual(open(mu.authors_filename).read(), 
                         'hi')

    def test_authors_file_is_created(self):
        self.assertEqual(
            self.mu.authors_filename,
            os.path.join(self.dir, 'bob',
                         'authors', 'authors.txt')
          )
        self.assertEqual(open(self.mu.authors_filename).read(), '')

    def test_set_authors_backs_up_file(self):
        def read_backup(num):
            filename = os.path.join(self.mu.authors_dir,
                                    'authors.txt.backup.%d' % num)
            return open(filename).read()

        self.mu.set_authors('foo')
        self.mu.set_authors('bar')
        self.mu.set_authors('baz')

        self.assertEqual(open(self.mu.authors_filename).read(), 'baz')
        self.assertEqual(read_backup(1), '')
        self.assertEqual(read_backup(2), 'foo')
        self.assertEqual(read_backup(3), 'bar')

    def test_get_issue_history(self):
        def mkissue(n, pubdate):
            name = os.path.join(self.mu.issues_dir, 'issue-%d.json' % n)
            open(name, 'w').write('{"pubDate": %s}' % repr(pubdate))
        
        self.assertEqual(len(self.mu.get_issue_history()), 0)
        mkissue(1, [2010, 1, 1])
        mkissue(2, [2010, 1, 2])
        history = self.mu.get_issue_history()
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0].number, 1)
        self.assertTrue(isinstance(history[0].pub_date,
                                   datetime.datetime))
        self.assertEqual(history[0].pub_date,
                         datetime.datetime(2010, 1, 1))
        self.assertEqual(history[1].number, 2)
        self.assertEqual(history[1].pub_date,
                         datetime.datetime(2010, 1, 2))

    def test_publish_edition_is_synchronized(self):
        filename = os.path.join(self.mu.root_user_dir, 'locked.lck')

        def publish_edition(**passed_kwargs):
            self.assertTrue(os.path.exists(filename))
            
        self.assertFalse(os.path.exists(filename))
        self.mu.publish_edition(publish_edition=publish_edition)
        self.assertFalse(os.path.exists(filename))

    def test_publish_edition_works(self):
        kwargs = {}
        
        def publish_edition(**passed_kwargs):
            kwargs.update(passed_kwargs)
        
        self.mu.publish_edition(people='passed through',
                                update_urls=True,
                                publish_edition=publish_edition)
        self.assertEqual(kwargs['people'], 'passed through')
        self.assertEqual(kwargs['output_dir'], self.mu.issues_dir)
        self.assertEqual(kwargs['cache_dir'], self.mu.caches_dir)
        self.assertEqual(kwargs['update_urls'], True)
        self.assertEqual(kwargs['authors_filename'], self.mu.authors_filename)
        