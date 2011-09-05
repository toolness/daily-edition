from fabric.api import *

try:
    import fabfile_local
except ImportError:
    pass

PROJ_ROOT = 'daily-edition'

def run_manage_cmd(cmd):
    with cd('%s/de_site' % PROJ_ROOT):
        run('python manage.py %s' % cmd)

def server(cmd):
    run('my-servers.py daily_edition %s' % cmd, pty=False)

@task
def status():
    server('status')

@task
def deploy():
    server('stop')
    with cd(PROJ_ROOT):
        run('git pull')
    run_manage_cmd('collectstatic --noinput')
    server('start')
