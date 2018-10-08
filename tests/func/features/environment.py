import os

import docker


def before_all(context):
    context.docker = docker.from_env()
    context.image_name = os.environ['IMAGE_NAME']
