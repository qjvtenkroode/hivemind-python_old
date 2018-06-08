from fabric.api import local, hide
from fabric.colors import red, green, yellow

projectsfolder = '~/playground/active'
project = 'hivemind'
p = '{}/{}'.format(projectsfolder,project)

def bootstrap():
    with hide('stdout', 'stderr'):
        try:
            local('ls -l {p}/env'.format(p=p))
        except:
            local('python3 -m venv {p}/env'.format(p=p))
        local('{p}/env/bin/pip install -r dev_requirements.txt'.format(p=p))

def bootstrap_travisci():
    local('pip install -r dev_requirements.txt')

def clean():
    print(yellow('removing temporary files:\n'))
    local('find . -name "*.pyc" -exec rm -f {} +')
    local('find . -name "*.pyo" -exec rm -f {} +')
    local('find . -name "__pycache__" -exec rm -rf {} +')
    print(green('done', bold=True))

def freeze():
    print(yellow('freezing pip requirements'))
    local('{p}/env/bin/pip freeze | sort > dev_requirements.txt'.format(p=p))
    local('{p}/env/bin/pip freeze | sort > requirements.txt'.format(p=p))
    print(green('done freezing requirements'))

def test(ci=None):
    print(yellow('starting test suite with pytest'))
    if ci == None:
        local('{p}/env/bin/pytest'.format(p=p))
    elif ci == 'travis-ci':
        local('pytest')
    else:
        print(red('unknown CI state', bold=True))
    print(green('done with test suite'))
