import pytest

from klander_core import kubectl


resource_example = dict(
    apiVersion='v1',
    kind='Pod',
    metadata=dict(
        namespace='default',
        name='example'
    )
)


@pytest.mark.proc_output('example')
def test_delete_success(mock_popen, mock_tempfile, mock_build_cmd):
    result = kubectl.delete(resource_example)

    assert result == 'example'
    mock_build_cmd.called_with(
        'delete',
        'v1', 'Pod',
        'default', 'example',
        output='name'
    )


@pytest.mark.proc_exit_code(1)
@pytest.mark.proc_output('error')
def test_delete_failure(mock_popen, mock_tempfile):
    with pytest.raises(RuntimeError) as exc_info:
        kubectl.delete(resource_example)

    assert str(exc_info.value) == 'error'
