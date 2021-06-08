import pytest

from . import data as test_data
from . import utils

from klander_core import reconciler


@pytest.mark.parametrize(
    'reconciler_resource',
    test_data.reconcilers[1:]
)
def test_reconciliation(
    mock_kubectl,
    mock_requests,
    capsys,
    reconciler_resource
):
    assertions = getattr(
        utils,
        reconciler_resource['metadata']['name']
    )

    reconciler_object = reconciler.Reconciler(reconciler_resource)

    observed_resources = reconciler_object.observe()
    assertions.observe(observed_resources)

    non_compliant_resources = reconciler_object.match(observed_resources)
    assertions.match(non_compliant_resources)

    reconciler_object.reconcile(non_compliant_resources)
    assertions.reconcile(capsys)
