#!/bin/bash
mkdir -p /course/11
kubectl create namespace secret --dry-run=client -o yaml | kubectl apply -f -
cat <<EOF > /course/11/secret1.yaml
apiVersion: v1
kind: Secret
metadata:
  name: secret1
  namespace: secret
type: Opaque
data:
  key: dGVzdAo=
EOF
