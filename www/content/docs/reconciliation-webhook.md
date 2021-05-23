+++
weight = 3
title = "Reconciliation Webhook"
description = """
Learn how to implement your own reconciliation webook to delegate the
reconciliation logic to a third-party service.
"""
toc = true
markup = "mmark"
+++

# Overview

The reconciliation Webhook is an HTTP server, listening for `POST` requests from
**klander**.

It allows you to implement a complex business logic to determine the
reconciliation action to take.

# Request/Response Schema

## State Reconciliation Request

On each resource needing reconciliation, a `POST` request will be sent to the
specified webhook.

The following body will be sent as JSON:

```yaml
apiVersion: datapio.co/v1
kind: StateReconciliationRequest
spec:
  object: # the non-compliant resource
```

## State Reconciliation Response

The webhook's response **MUST** be a JSON object validating this schema:

{.table .is-bordered .is-striped .is-hoverable .is-fullwidth}
| API Group | Version | Kind |
| --- | --- | --- |
| `datapio.co` | `v1` | `StateReconciliationResponse` |

{.table .is-bordered .is-striped .is-hoverable .is-fullwidth}
| Field | Type | Description |
| --- | --- | --- |
| `apiVersion` | string | Kubernetes resource API version |
| `kind` | string | Kubernetes resource kind |
| `spec` | [Response Spec](#response-spec) | Specification of the desired behavior |

## Response Spec

### Delete reconciliation

{.table .is-bordered .is-striped .is-hoverable .is-fullwidth}
| Field | Type | Description |
| --- | --- | --- |
| `delete` | boolean | If true, non-compliant resources will be deleted |

### Patch reconciliation

{.table .is-bordered .is-striped .is-hoverable .is-fullwidth}
| Field | Type | Description |
| --- | --- | --- |
| `patch` | object | The patch to apply on each non-compliant resources |
