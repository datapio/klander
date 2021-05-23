+++
weight = 1
title = "Getting Started"
description = """
Write your first compliance project and reconcile your Kubernetes cluster in
less than 5 minutes.
"""
toc = true
+++

# Overview

**klander** is a *Compliance-As-Code* utility. It allows you to detect
divergences from your desired [Kubernetes](https://kubernetes.io) cluster state
and perform reconciliation.

It works by specifying Kubernetes Resources to observe and how the should be
reconcilied if they are not compliant to your specification.

# Installation

## With Docker

```shell
$ docker pull ghcr.io/datapio/klander:latest
```

## Build from sources

If you wish to build *klander* from sources, you will need:

 - [Poetry](https://python-poetry.org/) to install the Python dependencies
 - [GNU Make](https://www.gnu.org/software/make/) to run the installation steps

Then run:

```shell
$ git clone https://github.com/datapio/klander
$ cd klander
$ make
```

This will use [PyInstaller](https://www.pyinstaller.org/) to build a standalone
executable, which will be located in the `dist` folder:

 - `klander` for UNIX platforms (Mac, Linux, BSD, ...)
 - `klander.exe` for Windows platforms

> **NB:** **klander** relies on the system's `kubectl` binary, please consult
> [this page](https://kubernetes.io/docs/tasks/tools/#kubectl) to install it.

## Install the CRDs

Before running **klander**, you will need to install the Kubernetes Custom
Resource Definitions:

```shell
$ kubectl apply -f https://raw.githubusercontent.com/datapio/klander/main/crds/state-reconciler.yml
```

# Reconcile your cluster

Create a file named `only-default-service-accounts.yml` with the following
content:

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

Then run:

```shell
$ kubectl apply -f only-default-service-accounts.yml
$ docker run \
      -v $HOME/.kube:/workspace/.kube \
      ghcr.io/datapio/klander:latest
```

This will remove every `ServiceAccount` whose name is not `default`.

# What's next?

Learn more about the [StateReconciler](/docs/state-reconciler/).
