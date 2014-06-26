import os
import shutil
from setuptools import setup, find_packages

config_file = os.path.expanduser('~/.dockertoprc')

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
        README = f.read()
if not os.path.isfile(config_file):
        shutil.copyfile('dockertoprc.yaml', config_file)
requires = [
    'pyyaml',
    'docker-py',
    'logging',
    'psutil',
    ]

setup(name='dockertop',
        version='0.0',
        description='A toplike utility for Docker container monitoring',
        long_description=README,
        author='Bradley Cicenas',
        author_email='bradley.cicenas@gmail.com',
        keywords='docker, monitoring, top',
        packages=find_packages(),
        include_package_data=True,
        install_requires=requires,
        tests_require=requires,
        entry_points = {
        'console_scripts' : ['dockertop = dockertop.dockertop:main']
        }
)
