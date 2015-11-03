#!/usr/bin/python
import subprocess, os, sys, shutil
from itertools import chain

def run(*args):
    ret = subprocess.call(args,  stdout=sys.stdout, stderr=sys.stderr)
    if ret != 0:
        exit(ret)

token = os.environ['GH_TOKEN']
repo = os.environ['TRAVIS_REPO_SLUG']
email = os.environ['USER_EMAIL']
name = os.environ['USER_NAME']

print('uploading site...')
run('git', 'config', 'user.email', email)
run('git', 'config', 'user.name', name)

print('checkout to master')
run('git', 'checkout', '--orphan', 'master')

print('clean up directory')
for (dirpath, dirnames, filenames) in os.walk("."):
    for folder in dirnames:
        if folder not in ['public', '.git']:
            shutil.rmtree(folder)
    for filename in filenames:
        if filename != '.gitignore':
            os.remove(filename)
    break
for (path, dirnames, filenames) in os.walk("public"):
    for item in chain(dirnames, filenames):
        shutil.move(path + "/" + item, ".")
    break
shutil.rmtree('public')

print('push to git')
run('git', 'add', '-A')
run('git', 'commit', '-am', "generate content")
run('git', 'push', '-fq', 'https://%s@github.com/%s.git' % (token, repo), 'master')
