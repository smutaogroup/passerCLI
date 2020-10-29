# -*- coding: utf-8 -*-

import setuptools
from distutils.command.clean import clean
import os

class Initialize(clean):
    def run(self):
        # Execute the classic clean command
        super().run()

        # move trained models to root directory 
        os.system("rm -r ~/.passerModels")
        os.system("mkdir ~/.passerModels")
        os.system("cp -r passer/trainedmodels/* ~/.passerModels")


with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as req:
    required = req.read().splitlines()

setuptools.setup(
    name='passer',
    description="PASSer: Protein Allosteric Site Server CLI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version='0.0.1',
    url='https://github.com/HTian1997/passerCLI',
    author='Hao Tian',
    author_email='htian1997@gmail.com',
    license='MIT',
    packages=setuptools.find_packages(),
    install_requires=required,
    entry_points={'console_scripts':\
        'passer = passer.cli:entry_point'},
    zip_safe=False,
    cmdclass={"init": Initialize},
)
