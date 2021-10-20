from setuptools import setup, find_packages
import os
from pathlib import Path
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

# default value, so what's the point of a VERSION.txt file?
# well, other's can access it too!

# VERSION = "0.2.0"
# ROOT_DIR = Path(__file__).parent

# if __file__:
#     with open(os.path.join(ROOT_DIR, 'VERSION.txt')) as version_file:
#         VERSION = version_file.read().strip()
setup(
    name='Hapy',
    # version=VERSION, We may not need this anymore https://stackoverflow.com/a/65625285/10382407
    author='Emmanuel Segun-Lean',
    author_email=
    'core-team.435caa94544f383ce9a89fab69dafa5b.show-sender@streams.zulipchat.com',
    license='MIT',
    description='Basic Python using Hausa vocabulary',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/hapy-lang/hapy',
    py_modules=['scripts'],
    packages=find_packages(),
    install_requires=[requirements],
    include_package_data=True,
    python_requires='>=3.7',
    setup_requires=[
        "wheel"
    ],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "Intended Audience :: Education",
        "Topic :: Education",
        "Topic :: Software Development"
    ],
    entry_points='''
        [console_scripts]
        hapy=scripts.hapy_cli:cli
    ''')
