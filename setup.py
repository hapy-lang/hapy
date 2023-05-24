from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name='Hapy',
    version='0.5.2',
    author='Emmanuel Segun-Lean',
    author_email='emmanuel.segunlean@proton.me',
    license='MIT',
    description='Basic Python using Hausa vocabulary',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/hapy-lang/hapy',
    packages=find_packages(),
    install_requires=requirements,
    include_package_data=True,
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "Intended Audience :: Education",
        "Topic :: Education",
        "Topic :: Software Development",
    ],
    entry_points={
        'console_scripts': [
            'hapy=scripts.hapy_cli:cli',
        ],
    },
)
