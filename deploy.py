#!/usr/bin/python
import subprocess, os, sys
def run(*args):
    ret = subprocess.call(args,  stdout=sys.stdout, stderr=sys.stderr)
    if ret != 0:
        exit(ret)

token = os.environ['GH_TOKEN']
repo = os.environ['TRAVIS_REPO_SLUG']

print('uploading site...')
sys.stdout.flush()
run('git', 'push', '-fq', 'https://%s@github.com/%s.git' % (token, repo), 'master')
