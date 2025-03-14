#!/usr/bin/env python3

import unittest
from os import path, getcwd
from importlib import import_module as importm

# Import project modules needed
cwd = path.abspath(getcwd())
root = path.dirname(cwd)

importm(path.join((root, 'global_decorator'))
importm(path.join((root, 'influx', 'run_container'))

# TODO: Make sure import works and dont include a dir so that the container is ephimeral
class TestContainer(unittest.TestCase):

    def setUp(self):

        # Set up the dir and store variables
        self.container = InfluxContainer(data_path=path.join(root, 'data'),
                                         config_path=path.join(root, 'config'))




if __name__ == '__main__':

    unittest.main()
