+++
weight = 2
title = "StateReconciler CRD"
description = """
Discover how the state reconciliation process works and how to customize its
behavior.
"""
toc = true
markup = "mmark"
+++

# Overview

The `StateReconciler` resource allows you to specify:

 - what resources to observe
 - the pattern they should follow
 - the action to take if a non-compliant resource is detected

The current supported actions are:

 - deleting the non-compliant resources
 - patching the non-compliant resources
 - delegating the delete/patch decision to a Webhook

# Custom Resource Definition

{.table .is-bordered .is-striped .is-hoverable .is-fullwidth}
| API Group | Version | Kind | Namespaced |
| --- | --- | --- | --- |
| `datapio.co` | `v1` | `StateReconciler` | ❌ |

{.table .is-bordered .is-striped .is-hoverable .is-fullwidth}
| Field | Type | Description |
| --- | --- | --- |
| `apiVersion` | string | Kubernetes resource API version |
| `kind` | string | Kubernetes resource kind |
| `metadata` | object | Kubernetes resource metadata |
| `spec` | [State Reconciler Spec](#state-reconciler-spec) | Specification of the desired behavior |

## State Reconciler Spec

{.table .is-bordered .is-striped .is-hoverable .is-fullwidth}
| Field | Type | Description |
| --- | --- | --- |
| `observe` | [Observer Spec](#observer-spec) | Describe what set of Kubernetes resource to audit |
| `match` | [MatchPattern Spec](#matchpattern-spec) | Describe how to match the Kubernetes resource that are compliant |
| `reconcile` | [Reconciler Spec](#reconciler-spec) | Describe the action to take for non-compliant resources |

## Observer Spec

{.table .is-bordered .is-striped .is-hoverable .is-fullwidth}
| Field | Type | Description |
| --- | --- | --- |
| `apiVersion` | string | Kubernetes resource API version |
| `kind` | string | Kubernetes resource kind |
| `namespaces` | string or list of string | Either `'*'` (all namespaces) or a list of namespace |


## Match Pattern Spec

### oneOf pattern

{.table .is-bordered .is-striped .is-hoverable .is-fullwidth}
| Field | Type | Description |
| --- | --- | --- |
| `oneOf` | list of [Match Pattern Spec](#match-pattern-spec) | Will match if any of the sub-patterns match |

### allOf pattern

{.table .is-bordered .is-striped .is-hoverable .is-fullwidth}
| Field | Type | Description |
| --- | --- | --- |
| `allOf` | list of [Match Pattern Spec](#match-pattern-spec) | Will match if all of the sub-patterns match |

### Field pattern

{.table .is-bordered .is-striped .is-hoverable .is-fullwidth}
| Field | Type | Description |
| --- | --- | --- |
| `field` | string | [JSON Path](https://pypi.org/project/jsonpath-ng/) of a field within the audited resource |
| `where` | [Where Tuple](#where-tuple) | Describe the comparison to perform |

#### Where Tuple

Syntax:

```
[operator, value]
```

With:

 - `operator` as one of:
    - `$lt`: Lesser Than
    - `$lte`: Lesser Than or Equal
    - `$eq`: Equal
    - `$ne`: Not Equal
    - `$gte`: Greater Than or Equal
    - `$gt`: Greater Than
    - `$in`: Included in Array
    - `$nin`: Not Included in Array
 - `value` as any valid JSON data type

## Reconciler Spec

### Delete reconciliation

{.table .is-bordered .is-striped .is-hoverable .is-fullwidth}
| Field | Type | Description |
| --- | --- | --- |
| `deleteExtras` | boolean | If true, non-compliant resources will be deleted |


### Patch reconciliation

{.table .is-bordered .is-striped .is-hoverable .is-fullwidth}
| Field | Type | Description |
| --- | --- | --- |
| `patch` | object | The patch to apply on each non-compliant resources |

### Webhook reconciliation

{.table .is-bordered .is-striped .is-hoverable .is-fullwidth}
| Field | Type | Description |
| --- | --- | --- |
| `webhook` | string | URL to the webhook. The reconciler will delegate the decision to this webhook. |

# What's next?

Discover how to implement your own
[Custom Reconciliation Webhook](/docs/reconciliation-webhook/).
