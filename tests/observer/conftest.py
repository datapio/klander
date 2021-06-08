from unittest.mock import patch
import pytest


@pytest.fixture
def mock_kubectl(request):
    def fake_getter(api_version, kind, namespace=None, name=None):
        if namespace == '*':
            namespace = 'default'

        if namespace == 'failure':
            raise RuntimeError('error')

        else:
            return dict(items=[
                dict(
                    apiVersion=api_version,
                    kind=kind,
                    metadata=dict(namespace=namespace)
                )
            ])

    with patch('klander_core.observer.kubectl.get') as mock:
        mock.side_effect = fake_getter
        yield mock
