import pytest

from klander_core import kubectl


def test_run_success(mock_popen, mock_tempfile):
    result = kubectl._run(['some', 'command']).decode('utf-8')
    assert result == 'hello world'


@pytest.mark.proc_exit_code(1)
@pytest.mark.proc_output('error')
def test_run_failure(mock_popen, mock_tempfile):
    with pytest.raises(RuntimeError) as exc_info:
        kubectl._run(['some', 'command'])

    assert str(exc_info.value) == 'error'
