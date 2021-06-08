import pytest
import json

from klander_core import kubectl


resource_example = dict(
    apiVersion='v1',
    kind='Pod',
    metadata=dict(
        namespace='default',
        name='example'
    )
)

patch_example = dict(foo='bar')


@pytest.mark.proc_output(json.dumps(dict(foo='bar')))
def test_update_success(mock_popen, mock_tempfile, mock_build_cmd):
    result = kubectl.update(resource_example, patch_example)

    assert result == dict(foo='bar')
    mock_build_cmd.called_with(
        'patch',
        'v1', 'Pod',
        'default', 'example'
    )


@pytest.mark.proc_exit_code(1)
@pytest.mark.proc_output('error')
def test_update_failure(mock_popen, mock_tempfile):
    with pytest.raises(RuntimeError) as exc_info:
        kubectl.update(resource_example, patch_example)

    assert str(exc_info.value) == 'error'
