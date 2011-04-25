import os
import logging

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
    def __init__(self, root_dir, user):
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
            open(self.authors_filename, 'w').close()

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
        