from unittest.mock import MagicMock, patch
import pytest

from klander_core.kubectl import _build_cmd as original_build_cmd


@pytest.fixture
def mock_fake_proc(request):
    fake_proc = MagicMock()

    marker = request.node.get_closest_marker('proc_exit_code')

    if marker is None:
        fake_proc.wait.return_value = 0

    else:
        fake_proc.wait.return_value = marker.args[0]

    yield fake_proc


@pytest.fixture
def mock_popen(mock_fake_proc):
    with patch('klander_core.kubectl.subprocess.Popen') as MockPopen:
        MockPopen.return_value = mock_fake_proc
        yield MockPopen


@pytest.fixture
def mock_fake_file(request):
    fake_file = MagicMock()

    marker = request.node.get_closest_marker('proc_output')

    if marker is None:
        fake_file.read.return_value = 'hello world'.encode('utf-8')

    else:
        fake_file.read.return_value = marker.args[0].encode('utf-8')

    yield fake_file


@pytest.fixture
def mock_tempfile(mock_fake_file):
    with patch('klander_core.kubectl.tempfile.TemporaryFile') as MockTempFile:
        context_manager = MagicMock()
        context_manager.__enter__.return_value = mock_fake_file
        MockTempFile.return_value = context_manager
        yield MockTempFile


@pytest.fixture
def mock_build_cmd():
    with patch('klander_core.kubectl._build_cmd') as fake_build_cmd:
        fake_build_cmd.side_effect = original_build_cmd
        yield fake_build_cmd
