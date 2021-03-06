state_reconciliation_responses = [
    (
        dict(
            apiVersion='datapio.co/v1',
            kind='StateReconciliationResponse',
            spec=dict(delete=True)
        ),
        True
    ),
    (
        dict(
            apiVersion='datapio.co/v1',
            kind='StateReconciliationResponse',
            spec=dict(patch=dict(spec=dict(serviceAccountName='default')))
        ),
        True
    ),
    (
        dict(
            apiVersion='wrong.datapio.co/v1',
            kind='StateReconciliationResponse',
            spec=dict(delete=True)
        ),
        False
    ),
    (
        dict(
            apiVersion='datapio.co/v1',
            kind='StateReconciliationResponseWrong',
            spec=dict(delete=True)
        ),
        False
    ),
    (
        dict(
            apiVersion='datapio.co/v1',
            kind='StateReconciliationResponse',
            spec=dict(webhook='https://example.com/not-expected-here')
        ),
        False
    )
]
