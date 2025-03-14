import docker
from os import path, mkdir
import logging
from secrets import token_bytes
from base64 import b64encode


class InfluxContainer:
    """
    Create an InfluxDB container that will connect to Grafana.
    """

    def __init__(self, data_path: str, config_path: str) -> None:
        """
        Create the data directory and connect to the Docker daemon

        Args:
            data_path (str): Path to the data directory
            config_path (str): Path to the config directory
        
        Returns:
            None
        """

        # Verify data path exists
        self.data_path = data_path
        if not path.exists(self.data_path):
            # Create path
            mkdir(self.data_path)
            logging.info(f'Created data path: {self.data_path}')

        # Verify config path exists
        self.config_path = config_path
        if not path.exists(self.config_path):
            # Create path
            mkdir(self.config_path)
            logging.info(f'Created data path: {self.config_path}')

        # Generate 256 bit (32 bytes) password and secret token as a byte string
        self.password = token_bytes(32)
        self.token = token_bytes(32)

        # Define the port mapping
        self.ports = {'8086/tcp': 8086}
        # Define the volume mapping, using the current working directory
        self.volumes = {
            self.data_path: {'bind': '/var/lib/influxdb2', 'mode': 'rw'},
            self.config_path: {'bind': '/etc/influxdb2', 'mode': 'rw'}
        }
        # Define environment variables
        self.environment = {
            "DOCKER_INFLUXDB_INIT_MODE": "setup",
            "DOCKER_INFLUXDB_INIT_USERNAME": "gadmin",
            "DOCKER_INFLUXDB_INIT_PASSWORD": b64encode(self.password).decode('utf-8'),
            "DOCKER_INFLUXDB_INIT_ORG": "ag_house",
            "DOCKER_INFLUXDB_INIT_BUCKET": "geigercounter",
            "DOCKER_INFLUXDB_INIT_ADMIN_TOKEN": b64encode(self.token).decode('utf-8')
        }


        # Connect to Docker daemon
        self.client = docker.from_env()


    def run(self, name: str):
        """
        Run the container

        Args:
            name (str): Name of the container
        
        Returns:
            XXXXXXX : Docker container object
        """

        self.name = name

        logging.debug(f'Container name: {self.name}')

        # Run the container in detached mode
        return self.client.containers.run(image="influxdb:2",
                                          detach=True,
                                          ports=self.ports,
                                          volumes=self.volumes,
                                          environment=self.environment,
                                          name=self.name)

    def __repr__(self):

        statement = f"""
Influx Container Parameters:
    Data Path: {self.data_path}
    Config Path: {self.config_path}
    Ports: {self.ports}
    Volumes: {self.volumes}
    Environment Variables: {self.environment}
"""

        return statement


if '__main__' == __name__:

    raise ImportError('THIS SHOULD ONLY BE IMPORTED')
