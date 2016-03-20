from setuptools import setup, find_packages

setup(
    name='django-filebased-email-backend-ng',
    version='2.0.2',
    description="A better 'file' email backend for Django",

    url="https://chris-lamb.co.uk/projects/django-filebased-email-backend-ng",
    author="Chris Lamb",
    author_email='chris@chris-lamb.co.uk',
    license="BSD",

    packages=find_packages(),

    install_requires=(
        'Django>=1.8',
    ),
)
