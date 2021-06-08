import pytest

from . import data as test_data

from klander_core import reconciler


def test_get_resources_success(mock_kubectl, capsys):
    items = reconciler.get_resources()
    capture = capsys.readouterr()

    assert len(items) == (len(test_data.reconcilers) - 1)
    assert 'Invalid StateReconciler resource:' in capture.err
    assert 'Unable to fetch resources:' not in capture.err


@pytest.mark.kubectl_get_raise(RuntimeError('error'))
def test_get_resources_failure(mock_kubectl, capsys):
    items = reconciler.get_resources()
    capture = capsys.readouterr()

    assert len(items) == 0
    assert 'Invalid StateReconciler resource:' not in capture.err
    assert 'Unable to fetch resources:' in capture.err
