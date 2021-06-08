"""
Observed Kubernetes resources fetcher.
"""

from typing import Union, List
from .kubectl import Resource

from . import kubectl

import sys


def get_resources(
    api_version: str,
    kind: str,
    namespaces: Union[str, List[str]]
) -> List[Resource]:
    """
    Get list of resources for each specified namespace.

    :param api_version: Kubernetes Resource API version (example: `batch/v1`)
    :param kind: Kubernetes Resource kind (example: `Job`)
    :param namespaces: Either `*` or a list of Kubernetes namespaces
    :return: List of successfully fetched Kubernetes resources.
    """

    if namespaces == '*':
        namespaces = ['*']

    resources = []

    for namespace in namespaces:
        try:
            items = kubectl.get(
                api_version=api_version,
                kind=kind,
                namespace=namespace
            )
            resources += items['items']

        except RuntimeError as err:
            print('Unable to fetch resources:', err, file=sys.stderr)

    return resources
