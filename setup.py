from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


def show_license():
    with open('LICENSE') as lice:
        return lice.read()


setup(name='observer_frontend',
      version='0.4',
      description='Frontend for iteratec\'s Observerhive Application',
      long_description=readme(),
      url='https://iteragit.iteratec.de/observer-hive/client-frontend.git',
      author='Masud Afschar',
      author_email='m.afschar@protonmail.com',
      license=show_license(),
      packages=['observer_frontend'],
      install_requires=[
          'flask',
          'flask_login',
          'flask_wtf',
          'wtforms',
          'bcrypt',
          'requests',
      ],
      include_package_data=True,
      scripts=['bin/observer-frontend'],
      zip_safe=False)
