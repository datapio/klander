from uuid import uuid4
import jsonschema
import requests
import json
import sys

from . import kubectl, observer, matcher, schema


def get_resources():
    def validate(resource):
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
        items = []

    return [item for item in items['items'] if validate(item)]


class Reconciler:
    def __init__(self, cr):
        self.cr = cr

    def observe(self):
        observer_meta = {
            'api_version': self.cr['spec']['observe']['apiVersion'],
            'kind': self.cr['spec']['observe']['kind'],
            'namespaces': self.cr['spec']['observe'].get('namespaces')
        }

        return observer.get_resources(**observer_meta)

    def match(self, resources):
        return [
            resource
            for resource in resources
            if not matcher.match_pattern(resource, self.cr['spec']['match'])
        ]

    def reconcile(self, resources):
        reconcile_method = cr['spec']['reconcile']

        if reconcile_method.get('deleteExtras'):
            for resource in not_matched:
                self._reconcile_delete(resource)

        elif reconcile_method.get('patch'):
            for resource in not_matched:
                self._reconcile_patch(resource, reconcile_method['patch'])

        elif reconcile_method.get('webhook'):
            for resource in not_matched:
                self._reconcile_webhook(resource, reconcile_method['webhook'])

        else:
            print('Invalid reconciliation method', file=sys.stderr)

    def _reconcile_delete(self, resource):
        try:
            resource_name = kubectl.delete(resource)
            print(resource_name, 'deleted')

        except RuntimeError as err:
            print('Unable to delete resource:', err, file=sys.stderr)

    def _reconcile_patch(self, resource, patch):
        try:
            patched = kubectl.patch(resource, patch)
            resource_name = f'{patched['kind']}/{patched['metadata']['name']}'
            print(resource_name, 'patched')

        except RuntimeError as err:
            print('Unable to patch resource:', err, file=sys.stderr)

    def _reconcile_webhook(self, resource, webhook):
        try:
            response = requests.post(webhook, json={
                'apiVersion': 'datapio.co/v1',
                'kind': 'StateReconciliationRequest',
                'spec': {
                    'object': resource
                }
            })
            response.raise_for_status()
            reconciliation_response = response.json()
            jsonschema.validate(
                reconciliation_response,
                schema.state_reconciliation_response
            )

        except requests.exceptions.RequestException as err:
            print('Unable to send request to webhook:', err, file=sys.stderr)

        except requests.exceptions.HTTPError as err:
            print('Webhook sent back an error:', err, file=sys.stderr)

        except json.JSONDecodeError as err:
            print('Unable to parse webhook response:', err, file=sys.stderr)

        except jsonschema.exceptions.ValidationError as err:
            print('Invalid webhook response:', err, file=sys.stderr)

        else:
            if reconciliation_response['spec'].get('delete'):
                self._reconcile_delete(resource)

            elif reconciliation_response['spec'].get('patch'):
                self._reconcile_patch(resource, reconciliation_response['patch'])

            else:
                print(
                    'Invalid reconciliation method from webhook',
                    file=sys.stderr
                )
