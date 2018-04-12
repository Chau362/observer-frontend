#!/usr/bin/env python
# # -*- coding: utf-8 -*-

""" This module can register and unregister projects at iteratec's Observerhive.
"""

import socket
import requests
import json

import logging


# logging setup
logger = logging.getLogger(__name__)
logger.setLevel('INFO')
logger_file_handler = logging.FileHandler('info.log')
logger_file_handler.setLevel('INFO')
logger_file_handler.setFormatter(
    logging.Formatter("%(asctime)s - [%(levelname)s] - %(name)s: %(message)s",
                      datefmt='%Y-%m-%d %H:%M:%S'))
console_log = logging.StreamHandler()
console_log.setLevel('INFO')
console_log.setFormatter(
    logging.Formatter("%(asctime)s - [%(levelname)s] - %(name)s: %(message)s",
                      datefmt='%Y-%m-%d %H:%M:%S'))
logger.addHandler(logger_file_handler)
logger.addHandler(console_log)


# load configs
with open('config.json') as json_data_file:
    configs = json.load(json_data_file)


class MyHTTPRequester:
    """This class contains functions to interact with the Conductor Service.
    """

    def __init__(self, service_address, port='5000'):
        self.port = port                        # Port number at which requests can be sent
        self.service_address = service_address  # Address of the Conductor Service


    @property
    def get_my_ip(self):
        """Function to find out internal IPv4-Address.
        """
        # get the current IP address of this machine
        my_ip = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2]
                   if not ip.startswith("127.")] or [
                      [(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close())
                       for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][
                          1]]) + ["no IP found"])[0]
        # IPv6 ?????
        # convert result into full address for webservices
        my_full_address = 'http://' + my_ip + ':' + self.port
        return my_full_address

    def register(self, event_type, project):
        """Function to register a specific event for one project.
        """
        my_full_address = "http://192.168.4.46:5000/event/"
        registration_parameters = {"eventType": event_type,
                                   "project": project,
                                   "projectUrl": "https://iteragit.iteratec.de/observer-hive/scab-oberserver-hive.git",
                                   "callback": my_full_address}
        # keep track while developing
        try:
            response = requests.post(self.service_address,
                                     json=registration_parameters,
                                     timeout=5)
            if response.status_code == 200:
                logger.info("Received the ID " + str(response.text) + " for " +
                            project + " concerning " + event_type + ".")
                return response.status_code
            else:
                print("Could not register " + event_type + " for "
                             + project + " due to fail at service.")
                return response.status_code
        except:
            print("Could not register " + event_type + " for "
                         + project + ".")
            return None

    def unregister(self, event_type, project):
        """Function to unregister a specific event for one project.
        """
        my_full_address = self.get_my_ip
        unregistration_parameters = {"eventType": event_type,
                                                "project": project,
                                                "Callback": my_full_address}
        response = requests.post(self.service_address,
                                 json=unregistration_parameters,
                                 timeout=5)
        print(response.text)