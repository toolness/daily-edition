import os
import tempfile
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

    def test_authors_file_is_created(self):
        self.assertEqual(
            self.mu.authors_filename,
            os.path.join(self.dir, 'bob',
                         'authors', 'authors.txt')
          )
        self.assertEqual(open(self.mu.authors_filename).read(), '')
