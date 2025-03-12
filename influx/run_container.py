import docker

client = docker.from_env()

# Define the container's name
container_name = "influxdb"

# Define the port mapping
ports = {'8086/tcp': 8086}

# Define the volume mapping, using the current working directory
volumes = {
    "$PWD/data": {'bind': '/var/lib/influxdb2', 'mode': 'r'},
    "$PWD/config": {'bind': '/etc/influxdb2', 'mode': 'r'}
}

# Define environment variables
environment = {
    "DOCKER_INFLUXDB_INIT_MODE": "setup",
    "DOCKER_INFLUXDB_INIT_USERNAME": "<USERNAME>",
    "DOCKER_INFLUXDB_INIT_PASSWORD": "<PASSWORD>",
    "DOCKER_INFLUXDB_INIT_ORG": "<ORG_NAME>",
    "DOCKER_INFLUXDB_INIT_BUCKET": "<BUCKET_NAME>"
}

# Run the container in detached mode
container = client.containers.run("influxdb:2", detach=True, ports=ports,
                                  volumes=volumes, environment=environment,
                                  name=container_name)
