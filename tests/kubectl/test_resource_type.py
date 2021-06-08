import pytest

from klander_core import kubectl

from . import data as test_data


@pytest.mark.parametrize(
    'api_version,kind,expected_type',
    test_data.resource_type
)
def test_get_resource_type(api_version, kind, expected_type):
    result = kubectl._get_resource_type(api_version, kind)
    assert result == expected_type
