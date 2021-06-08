import pytest

from klander_core import kubectl

from . import data as test_data


@pytest.mark.parametrize(
    'args,kwargs,expected_command',
    test_data.commands
)
def test_build_command(args, kwargs, expected_command):
    result = kubectl._build_cmd(*args, **kwargs)
    assert ' '.join(result) == ' '.join(expected_command)
