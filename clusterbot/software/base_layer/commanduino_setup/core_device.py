"""
.. module:: core_device
    :platform: Unix, Windows
    :synopsis: Baseline Commanduino implementation for primed Arduino boards

.. moduleauthor:: Graham Keenan <https://github.com/ShinRa26>

"""

import os
import sys
import json
import time
import inspect

from commanduino import CommandManager

HERE = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

root_path = os.path.join(HERE, "..", "..")
sys.path.append(root_path)

from utils import json_utils

""" CONSTANTS """
DEVICES = "devices"


class CommanduinoInitError(Exception):
    """
    Exception for handling Commanduino initialisation errors
    """
    pass


class CoreDevice(object):
    """
    Class representing a core Commanduino system.
    Allows access to the modules attached

    Args:
        config (str): path to the Commanduino config file
    """
    def __init__(self, config):
        self.mgr = CommandManager.from_configfile(config)
        self.config = json_utils.read(config)
        # self.devices = self.config[DEVICES].keys()
        self.devices = self.mgr.devices.keys()


    def valid_device(self, dev_name):
        """
        Checks if the given device name is present within the config

        Args:
            dev_name (str): name of the device
        
        Returns:
            valid (bool): If the device is present or not
        """
        return dev_name in self.devices

    def get_device_attribute(self, dev_name):
        """
        Gets the device attribute from CommandManager

        Args:
            dev_name (str): Name of the device

        Returns:
            device (CommandDevice): Device instance in the CommandManager

        Raises:
            AttributeError: The device is not in the CommandManager
        """
        if self.valid_device(dev_name):
            try:
                return getattr(self.mgr, dev_name)
            except AttributeError:
                print("No device named {0} in the manager!\nBailing out!".format(dev_name))
                sys.exit(-1)
        else:
            print("Invalid device name: {0}".format(dev_name))
            sys.exit(-1)
