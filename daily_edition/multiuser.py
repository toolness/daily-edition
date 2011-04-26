import os
import re
import glob
import logging
from datetime import datetime

class IssueMetadata(object):
    def __init__(self, path):
        self.number = int(re.match(r'.*issue-(\d+)\.json$', path).group(1))
        self.pub_date = datetime.fromtimestamp(os.stat(path).st_ctime)

    def __cmp__(self, other):
        return cmp(self.pub_date, other.pub_date)

def backup_file(filename):
    def mkfilename(i):
        return '%s.backup.%d' % (filename, i)

    i = 1
    backup_filename = mkfilename(i)
    while os.path.exists(backup_filename):
        i += 1
        backup_filename = mkfilename(i)

    contents = open(filename).read()
    open(backup_filename, 'w').write(contents)
    return backup_filename

class Account(object):
    def __init__(self, root_dir, user, default_authors=''):
        if not os.path.exists(root_dir):
            os.mkdir(root_dir)

        self.root_user_dir = os.path.join(root_dir, user.username)
        self.authors_dir = os.path.join(self.root_user_dir, 'authors')
        self.caches_dir = os.path.join(self.root_user_dir, 'caches')
        self.issues_dir = os.path.join(self.root_user_dir, 'issues')
        self.authors_filename = os.path.join(self.authors_dir, 'authors.txt')

        dirs_to_create = [
            self.root_user_dir,
            self.authors_dir,
            self.caches_dir,
            self.issues_dir,
        ]
        
        for dirpath in dirs_to_create:
            if not os.path.exists(dirpath):
                logging.info('Creating directory: %s' % dirpath)
                os.mkdir(dirpath)

        if not os.path.exists(self.authors_filename):
            f = open(self.authors_filename, 'w')
            f.write(default_authors)
            f.close()

    def _get_issue_path(self, issue):
        if issue is None:
            basename = 'daily-edition.json'
        else:
            basename = 'issue-%s.json' % issue
        return os.path.join(self.issues_dir, basename)

    def has_issue(self, issue=None):
        return os.path.exists(self._get_issue_path(issue))

    def get_issue_json(self, issue=None):
        return open(self._get_issue_path(issue)).read()

    def get_issue_history(self):
        globber = os.path.join(self.issues_dir, 'issue-*.json')
        issues = [IssueMetadata(issue)
                  for issue in glob.glob(globber)]
        issues.sort()
        return issues

    def set_authors(self, contents):
        backup_file(self.authors_filename)
        open(self.authors_filename, 'w').write(contents)

    def publish_edition(self, publish_edition, **kwargs):
        publish_edition(
            output_dir=self.issues_dir,
            cache_dir=self.caches_dir,
            authors_filename=self.authors_filename,
            **kwargs
            )
        