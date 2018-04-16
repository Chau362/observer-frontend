#!/usr/bin/env python
# # -*- coding: utf-8 -*-

""" This module can register and unregister projects at iteratec's Observerhive.
"""

import requests
import json
import socket
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


class MyHTTPRequester:
    """This class contains functions to interact with the Conductor Service.
    """

    def __init__(self, port):
        self.port = port

    def get_my_ip(self):
        """Function to find out internal IPv4-Address.
        """
        # get the current IP address of this machine
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        my_ip = s.getsockname()[0]
        s.close()
        # convert result into full address for webservices
        my_full_address = 'http://' + my_ip + ':' + self.port
        return my_full_address

    def register(self, event_type, project, projectUrl, service_address):
        """Function to register a specific event for one project.
        """
        my_full_address = self.get_my_ip()
        registration_parameters = {"eventType": event_type,
                                   "project": project,
                                   "projectUrl": projectUrl,
                                   "callback": my_full_address}
        # keep track while developing
        try:
            response = requests.post(service_address,
                                     json=registration_parameters)
            if response.status_code == 200:
                logger.info("Received the ID " + str(response.text) + " for " +
                            project + " concerning " + event_type + ".")
                return str(response.text)
            else:
                logger.info("Could not register " + event_type + " for "
                             + project + " due to fail at service " + service_address + '.')
                return None
        except:
            logger.info("Could not register " + event_type + " for "
                         + project + ".")
            return None


    def unregister(self, service_address, id):
        """Function to unregister a specific event for one project.
        """
        unregistration_parameters = {"id": id}
        response = requests.post(service_address,
                                 json=unregistration_parameters)
        if response.status_code == 200:
            logger.info('Unregistered event with ID ' + id)


    def check_registrations(self, id_list, service_address):
        response = requests.get(service_address)
        if response.status_code == 200:
            registered_projects = json.loads(response.text)
            check = True
            for id in id_list:
                if id not in registered_projects:
                    check = False
                    break
                else:
                    pass
            return check
        else:
            logger.info(service_address + ' sent status code ' + str(response.status_code))
            return None