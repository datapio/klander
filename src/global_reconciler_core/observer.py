from . import kubectl

import sys


def get_resources(api_version, kind, namespaces=None):
    if namespaces is None:
        namespaces = []

    elif namespaces == '*':
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
