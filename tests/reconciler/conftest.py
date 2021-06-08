from unittest.mock import MagicMock, patch
import pytest

from . import data as test_data

import json as json_module
import requests


@pytest.fixture
def mock_kubectl_get(request):
    def fake_get(api_version, kind, namespace=None, name=None):
        marker = request.node.get_closest_marker('kubectl_get_raise')

        if marker is not None:
            raise marker.args[0]

        if kind == 'StateReconciler':
            return dict(items=test_data.reconcilers)

        else:
            return dict(
                items=getattr(test_data, f'{kind.lower()}_examples', [])
            )

    with patch('klander_core.reconciler.kubectl.get') as mock:
        mock.side_effect = fake_get
        yield mock


@pytest.fixture
def mock_kubectl_delete():
    def fake_delete(resource):
        name = resource['metadata']['name']

        if name == 'raise':
            raise RuntimeError(name)

        return name

    with patch('klander_core.reconciler.kubectl.delete') as mock:
        mock.side_effect = fake_delete
        yield mock


@pytest.fixture
def mock_kubectl_update():
    def fake_update(resource, patch):
        name = resource['metadata']['name']

        if name == 'raise':
            raise RuntimeError(name)

        return resource

    with patch('klander_core.reconciler.kubectl.update') as mock:
        mock.side_effect = fake_update
        yield mock


@pytest.fixture
def mock_kubectl(mock_kubectl_get, mock_kubectl_delete, mock_kubectl_update):
    module = MagicMock()
    module.get = mock_kubectl_get
    module.delete = mock_kubectl_delete
    module.update = mock_kubectl_update

    yield module


@pytest.fixture
def mock_requests():
    def fake_post(url, json=None):
        assert json is not None

        name = json['spec']['object']['metadata']['name']
        response = MagicMock()

        if name == 'invalid-json':
            def raise_json():
                raise json_module.JSONDecodeError('error', '', 0)

            response.json.side_effect = raise_json

        elif name == 'invalid-resp':
            response.json.return_value = dict()

        elif name == 'not-found':
            def raise_http_error():
                raise requests.exceptions.HTTPError('error')

            response.raise_for_status.side_effect = raise_http_error

        elif name == 'unreachable':
            raise requests.exceptions.RequestException('error')

        elif url.endswith('/delete-webhook'):
            response.json.return_value = dict(
                apiVersion='datapio.co/v1',
                kind='StateReconciliationResponse',
                spec=dict(delete=True)
            )

        elif url.endswith('/patch-webhook'):
            response.json.return_value = dict(
                apiVersion='datapio.co/v1',
                kind='StateReconciliationResponse',
                spec=dict(patch=dict(foo='bar'))
            )

        return response

    with patch('klander_core.reconciler.requests.post') as mock_post:
        mock_post.side_effect = fake_post
        yield mock_post
