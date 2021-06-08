import pytest
import json

from klander_core import kubectl


@pytest.mark.proc_output(json.dumps(dict(foo='bar')))
def test_get_success(mock_popen, mock_tempfile, mock_build_cmd):
    result = kubectl.get('v1', 'Pod', 'default', 'example')

    assert result == dict(foo='bar')
    mock_build_cmd.called_with('get', 'v1', 'Pod', 'default', 'example')


@pytest.mark.proc_exit_code(1)
@pytest.mark.proc_output('error')
def test_get_failure(mock_popen, mock_tempfile):
    with pytest.raises(RuntimeError) as exc_info:
        kubectl.get('v1', 'Pod', 'default', 'example')

    assert str(exc_info.value) == 'error'
