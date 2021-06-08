"""
Reconciliation workflow.
"""

from typing import List
from .kubectl import PartialResource, Resource

import jsonschema
import requests
import json
import sys

from . import kubectl, observer, matcher, schema


def get_resources() -> List[Resource]:
    """
    Fetch StateReconciler Kubernetes resources.

    :return: List of valid StateReconciler resources
    """

    def validate(resource: Resource) -> bool:
        """
        Validate a StateReconciler resource against its JSON schema.

        :return: True if the resource is valid, False otherwise
        """

        try:
            jsonschema.validate(resource, schema.state_reconciler)

        except jsonschema.exceptions.ValidationError as err:
            print('Invalid StateReconciler resource:', err, file=sys.stderr)
            return False

        else:
            return True

    try:
        items = kubectl.get(
            api_version='datapio.co/v1',
            kind='StateReconciler'
        )

    except RuntimeError as err:
        print('Unable to fetch resources:', err, file=sys.stderr)
        items = dict(items=[])

    return [item for item in items['items'] if validate(item)]


class Reconciler:
    """
    Reconiliation workflow executor.

    :ivar spec: StateReconciler resource associated to this executor.
    """

    spec: Resource

    """
    :param spec: StateReconciler resource to associate to this executor.
    """
    def __init__(self, spec: Resource):
        self.spec = spec

    def observe(self) -> List[Resource]:
        """
        Fetch observed Kubernetes resources by this StateReconciler.

        :return: List of successfully fetched resources
        """

        observer_meta = {
            'api_version': self.spec['spec']['observe']['apiVersion'],
            'kind': self.spec['spec']['observe']['kind'],
            'namespaces': self.spec['spec']['observe']['namespaces']
        }

        return observer.get_resources(**observer_meta)

    def match(self, resources: List[Resource]) -> List[Resource]:
        """
        Get list of non-compliant Kubernetes resources.

        :param resources: List of resources to validate
        :return: List of non-compliant resources
        """

        return [
            resource
            for resource in resources
            if not matcher.match_pattern(resource, self.spec['spec']['match'])
        ]

    def reconcile(self, resources: List[Resource]) -> None:
        """
        Perform the required action on non-compliant Kubernetes resources.

        :param resources: List of resources to correct
        """

        reconcile_method = self.spec['spec']['reconcile']

        if reconcile_method.get('deleteExtras'):
            for resource in resources:
                self._reconcile_delete(resource)

        elif reconcile_method.get('patch'):
            for resource in resources:
                self._reconcile_patch(resource, reconcile_method['patch'])

        elif reconcile_method.get('webhook'):
            for resource in resources:
                self._reconcile_webhook(resource, reconcile_method['webhook'])

    @staticmethod
    def _reconcile_delete(resource: Resource) -> None:
        """
        Delete the non-compliant Kubernetes resource.

        :param resource: Resource to delete
        """

        try:
            resource_name = kubectl.delete(resource)
            resource_kind = resource['kind']
            display_name = f'{resource_kind}/{resource_name}'.lower()
            print(display_name, 'deleted')

        except RuntimeError as err:
            print('Unable to delete resource:', err, file=sys.stderr)

    @staticmethod
    def _reconcile_patch(resource: Resource, patch: PartialResource) -> None:
        """
        Update the non-compliant Kubernetes resource.

        :param resource: Resource to modify
        :param patch: Modifications to apply
        """

        try:
            patched = kubectl.update(resource, patch)
            kind, name = patched['kind'], patched['metadata']['name']
            resource_name = f'{kind}/{name}'.lower()
            print(resource_name, 'patched')

        except RuntimeError as err:
            print('Unable to patch resource:', err, file=sys.stderr)

    def _reconcile_webhook(self, resource: Resource, webhook: str) -> None:
        """
        Delegate the reconciliation method (delete/patch) decision to a
        webhook.

        :param resource: Resource to send to the webhook
        :param webhook: Webhook URL
        """

        try:
            response = requests.post(webhook, json={
                'apiVersion': 'datapio.co/v1',
                'kind': 'StateReconciliationRequest',
                'spec': {
                    'object': resource
                }
            })
            response.raise_for_status()
            reconciliation_resp = response.json()
            jsonschema.validate(
                reconciliation_resp,
                schema.state_reconciliation_response
            )

        except requests.exceptions.HTTPError as err:
            print('Webhook sent back an error:', err, file=sys.stderr)

        except requests.exceptions.RequestException as err:
            print('Unable to send request to webhook:', err, file=sys.stderr)

        except json.JSONDecodeError as err:
            print('Unable to parse webhook response:', err, file=sys.stderr)

        except jsonschema.exceptions.ValidationError as err:
            print('Invalid webhook response:', err, file=sys.stderr)

        else:
            if reconciliation_resp['spec'].get('delete'):
                self._reconcile_delete(resource)

            elif patch := reconciliation_resp['spec'].get('patch'):
                self._reconcile_patch(resource, patch)
