"""
JSON schema for data validation.
"""

from .matcher import match_operators


state_reconciler = dict(
    type='object',
    required=['apiVersion', 'kind', 'metadata', 'spec'],
    definitions=dict(
        observer=dict(
            type='object',
            required=['apiVersion', 'kind', 'namespaces'],
            properties=dict(
                apiVersion=dict(type='string'),
                kind=dict(type='string'),
                namespaces=dict(
                    oneOf=[
                        dict(type='string', enum=['*']),
                        dict(type='array', items=dict(type='string'))
                    ]
                )
            )
        ),
        matcher=dict(
            type='object',
            oneOf=[
                dict(
                    required=['field', 'where'],
                    properties=dict(
                        field=dict(type='string'),
                        where=dict(
                            type='array',
                            items=[
                                dict(
                                    type='string',
                                    enum=list(match_operators.keys())
                                ),
                                dict()
                            ]
                        )
                    )
                ),
                dict(
                    required=['oneOf'],
                    properties=dict(
                        oneOf=dict(
                            type='array',
                            items={'$ref': '#/definitions/matcher'}
                        )
                    )
                ),
                dict(
                    required=['allOf'],
                    properties=dict(
                        allOf=dict(
                            type='array',
                            items={'$ref': '#/definitions/matcher'}
                        )
                    )
                )
            ]
        ),
        reconciler=dict(
            type='object',
            oneOf=[
                dict(
                    required=['deleteExtras'],
                    properties=dict(
                        deleteExtras=dict(type='boolean')
                    )
                ),
                dict(
                    required=['patch'],
                    properties=dict(
                        patch=dict(type='object')
                    )
                ),
                dict(
                    required=['webhook'],
                    properties=dict(
                        webhook=dict(type='string', format='url')
                    )
                )
            ]
        )
    ),
    properties=dict(
        apiVersion=dict(type='string', enum=['datapio.co/v1']),
        kind=dict(type='string', enum=['StateReconciler']),
        metadata=dict(
            type='object',
            required=['name'],
            properties=dict(
                name=dict(type='string')
            )
        ),
        spec=dict(
            type='object',
            required=['observe', 'match', 'reconcile'],
            properties=dict(
                observe={'$ref': '#/definitions/observer'},
                match={'$ref': '#/definitions/matcher'},
                reconcile={'$ref': '#/definitions/reconciler'}
            )
        )
    )
)

state_reconciliation_response = dict(
    type='object',
    required=['apiVersion', 'kind', 'spec'],
    properties=dict(
        apiVersion=dict(type='string', enum=['datapio.co/v1']),
        kind=dict(type='string', enum=['StateReconciliationResponse']),
        spec=dict(
            type='object',
            oneOf=[
                dict(
                    required=['delete'],
                    properties=dict(
                        delete=dict(type='boolean')
                    )
                ),
                dict(
                    required=['patch'],
                    properties=dict(
                        patch=dict(type='object')
                    )
                )
            ]
        )
    )
)
