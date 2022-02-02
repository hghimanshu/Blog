import os
from pathlib import Path
from time import sleep
from typing import Text

import click
import ray
from ray import serve


class RaySetupManager:
    def __init__(
        self, address: Text, namespace: Text, num_cpus: int
    ) -> None:
        self.address = address
        self.namespace = namespace
        self.ray_shutdown_command = "ray stop --force"
        self.num_cpus = num_cpus if num_cpus else 0

    def __enter__(self):
        ray.init(namespace=self.namespace, num_cpus=self.num_cpus)
        serve.start(
            detached=True,
        )

    def __exit__(self, *exc):
        os.system(self.ray_shutdown_command)


@click.command()
@click.option(
    "-n",
    "--namespace",
    type=click.STRING,
    default="serve",
    required=False,
    help="namespace for starting ray",
)
@click.option(
    "-a",
    "--address",
    type=click.STRING,
    required=False,
    default="auto",
    help="address for connecting to existing ray head",
)
@click.option(
    "-c",
    "--num-cpus",
    type=click.INT,
    default=2,
    required=False,
    help="address for connecting to existing ray head",
)
def start_ray_and_serve(
    namespace: Text, address: Text, num_cpus: int
):
    with RaySetupManager(
        address, namespace, num_cpus=num_cpus
    ) as _:
        while True:
            sleep(1)



if __name__ == "__main__":
    start_ray_and_serve()
