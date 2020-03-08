import os
from _utils import write_script, execute_bash_script


git_username = 'reneang17'
travis_user = 'reneang17'
git_repo_name = 'giter'
author = 'Rene Angeles'
author_email = 'reneang17@gmail.com'
package_name = 'Giter'


add_template_dirs = True
add_travis = True




############################################
## ------- Create readme
############################################

readme_content = \
"""# {}
""".format(package_name)
if add_travis:
    readme_content+=\
    "[![Build Status](https://travis-ci.com/{0}/{1}.svg?branch=master)](https://travis-ci.com/{0}/{1})\n".format(travis_user,git_repo_name)

write_script(dir = './', script_name = 'README.md',
    script_content = readme_content)


################################## = ##########
## ------- Create package
############################################

if not os.path.exists(package_name):
    os.makedirs(package_name)

init_content = "from .{} import *".format(package_name)
write_script(dir = package_name, script_name = '__init__.py',
    script_content = init_content)

inital_object = package_name+'_object'
package_content = \
"""class {}(object):
    def __init__(self):
        print('et print, ergo sum')

    def fizz(self):
        return 'buzz'
""".format(inital_object)
write_script(dir = package_name, script_name = package_name + '.py',
    script_content = package_content)



############################################
## ------- create/install setup file
############################################

url = ''.join(['https://github.com/',git_username, '/', git_repo_name])
packages = [package_name]
setup_dir = package_name
setup_content = \
"""from distutils.core import setup

setup(name = '{}',
author = '{}',
author_email = '{}',
url = '{}',
packages = {}
)
""".format(git_repo_name, author, author_email, url, packages)
write_script('./', 'setup.py', setup_content)


############################################
## ------- Add test
############################################

if not os.path.exists('test'):
    os.makedirs('test')
test_file_name = 'test_' + package_name + '.py'
test_content = \
"""import numpy as np
import numpy.testing as npt

import {0}

def test_{0}_smoke():
    #Smoke_test
    obt = {0}.{1}()

def test_{1}_fizz():
    #test the fizz_function
    obj = {0}.{1}()
    output = obj.fizz()

    npt.assert_equal(output, "buzz")
""".format(package_name, inital_object)

write_script('./test', test_file_name, test_content)


################################## = ##########
## ------- Add python based template folders
############################################

template_dirs = ['data', 'notebooks']
if add_template_dirs:
    for dir in template_dirs:
        if not os.path.exists(dir):
            os.makedirs(dir)


############################################
## ------- Install Package, test, Push to github
############################################

github_bash_content = \
"""#!/bin/bash
pip install requirements.txt
python setup.py install && pytest
git init
git add .
git add -f ./{}/__init__.py
""".format(package_name)

if add_travis:
    github_bash_content+='git add -f .travis.yml\n'
if add_template_dirs:
    for dir in template_dirs:
        github_bash_content+="""cp .gitignore {}\n""".format(dir)
        github_bash_content+="""git add {}\n""".format(dir)

github_bash_content+="""
#git commit -m "first commit"
#git remote add origin {}.git
#git push -u origin master
""".format(url)

write_script('.', '_first_commit.sh', github_bash_content)
execute_bash_script('./', '_first_commit.sh')