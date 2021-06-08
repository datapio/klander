import pytest

from klander_core.matcher import match_pattern
from . import data as test_data



@pytest.mark.parametrize(
    'value,pattern,match',
    test_data.patterns
)
def test_pattern_matching(value, pattern, match):
    result = match_pattern(value, pattern)
    assert result == match
