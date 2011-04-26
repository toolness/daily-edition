import subprocess
import sys
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
path = lambda *a: os.path.join(ROOT, *a)

requirements = path('..', 'requirements.txt')
req_contents = open(requirements, 'r').read()
install_requires = req_contents.splitlines()

def bootstrap():
    '''
    This sets up a virtualenv and installs all our dependencies
    into it.
    '''

    vdir = path('..', '.virtualenv')
    if not os.path.exists(vdir):
        subprocess.check_call([sys.executable, path('virtualenv.py'),
                               vdir])

    # See if our dependencies changed since we last looked at them.
    last_requirements = path(vdir, 'requirements.txt')
    last_req_contents = ''
    if os.path.exists(last_requirements):
        last_req_contents = open(last_requirements, 'r').read()
    if req_contents != last_req_contents:
        pip = path(vdir, 'bin', 'pip')
        
        # Install the dependencies with pip.
        subprocess.check_call([pip, 'install', '-r', requirements])

        open(last_requirements, 'w').write(req_contents)

    # Activate the virtualenv. (Code taken from virtualenv docs.)
    activate_this = path(vdir, 'bin', 'activate_this.py')
    execfile(activate_this, dict(__file__=activate_this))
