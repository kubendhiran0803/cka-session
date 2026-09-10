#!/bin/bash
mkdir -p /course/17/operator/base /course/17/operator/prod
cat <<EOF > /course/17/operator/base/kustomization.yaml
resources:
- role.yaml
EOF
cat <<EOF > /course/17/operator/base/role.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: operator-role
  namespace: default
rules: []
EOF
cat <<EOF > /course/17/operator/prod/kustomization.yaml
resources:
- ../base
EOF
