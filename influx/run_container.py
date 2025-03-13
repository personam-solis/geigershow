import docker
from os import path, mkdir
import logging
from secrets import token_bytes
from base64 import b64encode

class InfluxContainer:
    """
    Create an InfluxDB container that will connect to Grafana.
    """

    def __init__(self, data_path):
        """
        Create the data directory and connect to the Docker daemon

        Args:
            data_path (str): Path to the data directory
        
        Returns:
            None
        """

        # Verify path
        self.data_path = data_path
        logging.debug(f'Data path: {data_path}')

        if not path.exists(data_path):
            # Create path
            mkdir(data_path)
            logging.info(f'Created data path: {data_path}')

        # Generate 32 bit password as bytes
        self.password = token_bytes(32)

        # Define the container's name
        self.container_name = "influxdb"
        # Define the port mapping
        self.ports = {'8086/tcp': 8086}
        # Define the volume mapping, using the current working directory
        self.volumes = {
            "$PWD/data": {'bind': '/var/lib/influxdb2', 'mode': 'r'},
            "$PWD/config": {'bind': '/etc/influxdb2', 'mode': 'r'}
        }
        # Define environment variables
        self.environment = {
            "DOCKER_INFLUXDB_INIT_MODE": "setup",
            "DOCKER_INFLUXDB_INIT_USERNAME": "gadmin",
            "DOCKER_INFLUXDB_INIT_PASSWORD": b64encode(self.password).decode('utf-8'),
            "DOCKER_INFLUXDB_INIT_ORG": "ag_house",
            "DOCKER_INFLUXDB_INIT_BUCKET": "geigercounter"
        }


        # Connect to Docker daemon
        self.client = docker.from_env()


    def run(self, name):
        """
        Run the container

        Args:
            name (str): Name of the container
        
        Returns:
            None
        """

        self.name = name

        logging.debug(f'Container name: {self.name}')

        # Run the container in detached mode
        self.container = self.client.containers.run("influxdb:2", detach=True,
                                                    ports=self.ports,
                                                    volumes=self.volumes,
                                                    environment=self.environment,
                                                    name=self.container_name)
        self.container_id = self.container.id
        logging.debug(f'Container running with ID: {self.container_id}')

    def __repr__(self):

        statement = f"""
Influx Container Parameters:
    Data Path: {self.data_path}
    Container Name: {self.container_name}
    Ports: {self.ports}
    Volumes: {self.volumes}
    Environment Variables: {self.environment}
"""

        return statement


if '__main__' == __name__:

    raise ImportError('THIS SHOULD ONLY BE IMPORTED')
