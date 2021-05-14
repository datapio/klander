from .matcher import match_operators


state_reconciler = {
    'type': 'object',
    'required': ['apiVersion', 'kind', 'metadata', 'spec'],
    'definitions': {
        'observer': {
            'type': 'object',
            'required': ['apiVersion', 'kind', 'namespaces'],
            'properties': {
                'apiVersion': {'type': 'string'},
                'kind': {'type': 'string'},
                'namespaces': {
                    'oneOf': [
                        {'type': 'string', 'enum': ['*']},
                        {'type': 'array', 'items': {'type': 'string'}}
                    ]
                }
            }
        },
        'matcher': {
            'type': 'object',
            'oneOf': [
                {
                    'required': ['field', 'where'],
                    'properties': {
                        'field': {'type': 'string'},
                        'where': {
                            'type': 'array',
                            'items': [
                                {
                                    'type': 'string',
                                    'enum': list(match_operators.keys())
                                },
                                {}
                            ]
                        }
                    }
                },
                {
                    'required': ['oneOf'],
                    'properties': {
                        'oneOf': {
                            'type': 'array',
                            'items': {'$ref': '#/definitions/matcher'}
                        }
                    }
                },
                {
                    'required': ['allOf'],
                    'properties': {
                        'allOf': {
                            'type': 'array',
                            'items': {'$ref', '#/definitions/matcher'}
                        }
                    }
                }
            ]
        },
        'reconciler': {
            'type': 'object',
            'oneOf': [
                {
                    'required': ['deleteExtras'],
                    'properties': {
                        'deleteExtras': {'type': 'boolean'}
                    }
                },
                {
                    'required': ['patch'],
                    'properties': {
                        'patch': {'type': 'object'}
                    }
                },
                {
                    'required': ['webhook'],
                    'properties': {
                        'webhook': {'type': 'string', 'format': 'url'}
                    }
                }
            ]
        }
    },
    'properties': {
        'apiVersion': {'type': 'string', 'enum': ['datapio.co/v1']},
        'kind': {'type': 'string', 'enum': ['StateReconciler']},
        'metadata': {
            'type': 'object',
            'required': ['name'],
            'properties': {
                'name': {'type': 'string'}
            }
        },
        'spec': {
            'type': 'object',
            'required': ['observe', 'match', 'reconcile'],
            'properties': {
                'observe': {'$ref': '#/definitions/observer'},
                'match': {'$ref': '#/definitions/matcher'},
                'reconcile': {'$ref': '#/definitions/reconciler'}
            }
        }
    }
}

state_reconciliation_response = {
    'type': 'object',
    'required': ['apiVersion', 'kind', 'spec'],
    'properties': {
        'apiVersion': {'type': 'string', 'enum': ['datapio.co/v1']},
        'kind': {'type': 'string', 'enum': ['StateReconciliationResponse']},
        'spec': {
            'type': 'object',
            'oneOf': [
                {
                    'required': ['delete'],
                    'properties': {
                        'delete': {'type': 'boolean'}
                    }
                },
                {
                    'required': ['patch'],
                    'properties': {
                        'patch': {'type': 'object'}
                    }
                }
            ]
        }
    }
}
