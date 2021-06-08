import pytest

from klander_core import observer


def test_get_all_success(mock_kubectl, capsys):
    result = observer.get_resources('v1', 'Pod', '*')

    assert result == [
        dict(
            apiVersion='v1',
            kind='Pod',
            metadata=dict(namespace='default')
        )
    ]

    captured = capsys.readouterr()
    assert len(captured.err) == 0


def test_get_success(mock_kubectl, capsys):
    result = observer.get_resources('v1', 'Pod', ['default', 'other'])

    assert result == [
        dict(
            apiVersion='v1',
            kind='Pod',
            metadata=dict(namespace='default')
        ),
        dict(
            apiVersion='v1',
            kind='Pod',
            metadata=dict(namespace='other')
        )
    ]

    captured = capsys.readouterr()
    assert len(captured.err) == 0


def test_get_failure(mock_kubectl, capsys):
    result = observer.get_resources('v1', 'Pod', ['default', 'failure'])
    assert result == [
        dict(
            apiVersion='v1',
            kind='Pod',
            metadata=dict(namespace='default')
        )
    ]

    captured = capsys.readouterr()
    assert len(captured.err) > 0
