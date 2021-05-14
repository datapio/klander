# klander

This project provides a command-line utility that allows you to:

 - specify a set of Kubernetes resources to audit
 - identify divergences from your desired cluster state
 - resolve those divergences

## Usage

A Custom Resource Definition is provided allowing you to declare the complete
reconciliation process, for example:

```yaml
---
apiVersion: datapio.co/v1
kind: StateReconciler
metadata:
  name: only-default-service-accounts
spec:
  observe:
    apiVersion: v1
    kind: ServiceAccount
    namespaces: '*'
  match:
    field: metadata.name
    where: ['$eq', 'default']
  reconcile:
    deleteExtras: yes
```

The above resource will delete every ServiceAccount whose name is not `default`.

See [the documentation](https://github.com/datapio/klander/wiki) for
more information.
