import pytest

from klander_core import schema

from . import data as test_data
from .utils import validate


@pytest.mark.parametrize(
    'resource,valid',
    test_data.state_reconcilers
)
def test_state_reconciler_validation(resource, valid):
    result = validate(resource, schema.state_reconciler)
    assert result is valid


@pytest.mark.parametrize(
    'resource,valid',
    test_data.state_reconciliation_responses
)
def test_state_reconciliation_response_validation(resource, valid):
    result = validate(resource, schema.state_reconciliation_response)
    assert result is valid
