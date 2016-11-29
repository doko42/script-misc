#!/usr/bin/env python3

import subprocess
import shutil
import os
from termcolor import colored

buffer = ''

def printme(string):
    global buffer
    buffer += string + '\n'
    print(string)

def create_dir(path):
    if os.path.exists(path):
        return
    os.makedirs(path)

tokens = ['error: ', 'internal compiler error: ', ' FAILED ']
extra_lines = 1

def grep_errors(log):
    lines = log.split('\n')
    for i, v in enumerate(lines):
        if any(map(lambda x: x in v, tokens)):
            v = ['  ' + x for x in lines[i - 1: i + 1]]
            printme('\n'.join(v))

project = 'openSUSE:Factory:Staging:Gcc7'
repository = 'standard'

log_dir = '/tmp/obs-logs'
shutil.rmtree(log_dir, ignore_errors = True)

def process_arch(arch):
    arch_dir = os.path.join(log_dir, arch)

    result = subprocess.check_output('osc r %s -r %s -a %s --csv' % (project, repository, arch), shell = True)
    packages = result.decode('utf-8').split('\n')
    failed = [x.split(';')[0] for x in packages if x.endswith(';failed')]

    create_dir(arch_dir)
    for package in sorted(failed):
        result = subprocess.check_output('osc remotebuildlog %s %s %s %s' % (project, package, repository, arch), shell = True)
        log = result.decode('utf-8')
        log_file = os.path.join(arch_dir, package + '.log')
        with open(log_file, 'w+') as w:
            w.write(log)
        printme(package)
        grep_errors(log)

for arch in ['x86_64', 'i586', 'ppc64le']:
    printme('== %s ==' % arch)
    process_arch(arch)

with open(os.path.join(log_dir, 'build.log'), 'w+') as w:
    w.write(buffer)