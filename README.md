# observer-hive: client frontend

This module is the client side server process of the observer-hive. It allows you to process events received
from webservices such as Gitlab, Jenkins and Sonarqube. If you are interested in the full project you should
take a look at its counterpart: the [conductor server](https://iteragit.iteratec.de/observer-hive/scab-oberserver-hive).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

This application is meant to run on a RaspberryPi. What should be installed:

* [Raspbian](https://www.raspberrypi.org/downloads/raspbian/) - the operating system on the RaspberryPi
* [Python 3.x](https://www.python.org) - usually comes with Raspbian

### Installing

#### Debian package

If you have downloaded the Debian package simply run

```
sudo dpkg -i client-frontend.deb
```

If this fails due to missing dependencies run

```
sudo apt-get -f install
```

You should now be good and ready.

## Running the tests

`pytest` has been setup as the test runner of this package. You can run the tests with the following command:

```
python3 setup.py test
```

## Deployment

...

## Built With

* [Flask](http://flask.pocoo.org/) - lightweight WSGI web application framework

## Versioning

We use [Gitlab](https://gitlab.com/) for versioning. For the versions available, see the [tags on this repository](https://iteragit.iteratec.de/observer-hive/client-frontend.git). 

## Authors

* **Gerd Neugebauer** - *Idea* - [gne](https://iteragit.iteratec.de/gne)
* **Masud Afschar** - *Initial work* - [mafschar](https://iteragit.iteratec.de/mafschar)

See also the list of [contributors](https://iteragit.iteratec.de/observer-hive/client-frontend/graphs/master) who participated in this project.

## License

This project is licensed under the BSD 3-Clause License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* Many thanks to **Chau** - [cpham](https://iteragit.iteratec.de/cpham) - for his constant help.