from typing import Any, Dict, List

from chaoslib.types import Configuration, Secrets
from chaosopenstack import openstack_client
from chaosopenstack.types import OpenstackResponse
from logzero import logger

__all__ = [
    "stop_instances",
    "start_instances",
]


def stop_instances(
    filters: List[Dict[str, Any]],
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> List[OpenstackResponse]:
    """
    Stop OpenStack instance(s)

    Instances are targeted by providing filters.
    https://docs.openstack.org/api-ref/compute/?expanded=list-servers-detail#list-servers
    """
    response = []

    client = openstack_client(configuration, secrets)
    instances = client.compute.servers(**filters)

    for instance in instances:
        if instance.status != "ACTIVE":
            logger.info(
                "Skip instance {} [{}] ({})".format(
                    instance.name, instance.id, instance.status
                )
            )
            continue

        logger.info("Stop instance {} [{}]".format(instance.name, instance.id))
        client.compute.stop_server(instance)
        response.append(instance.to_dict())


def start_instances(
    filters: List[Dict[str, Any]],
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> List[OpenstackResponse]:
    """
    Start OpenStack instance(s)

    Instances are targeted by providing filters.
    https://docs.openstack.org/api-ref/compute/?expanded=list-servers-detail#list-servers
    """
    response = []

    client = openstack_client(configuration, secrets)
    instances = client.compute.servers(**filters)

    for instance in instances:
        if instance.status != "SHUTOFF":
            logger.info(
                "Skip instance {} [{}] ({})".format(
                    instance.name, instance.id, instance.status
                )
            )
            continue

        logger.info("Start instance {} [{}]".format(instance.name, instance.id))
        client.compute.start_server(instance)
        response.append(instance.to_dict())
