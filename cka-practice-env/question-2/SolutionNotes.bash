#!/bin/bash
# 1. ssh cka2560
# 2. cd /etc/kubernetes/manifests
# 3. kubectl run my-static-pod --image=nginx:1-alpine --dry-run=client -o yaml > my-static-pod.yaml
# 4. Edit yaml to add resources: requests: cpu: 10m, memory: 20Mi
# 5. kubectl expose pod my-static-pod-cka2560 --name static-pod-service --type=NodePort --port=80
