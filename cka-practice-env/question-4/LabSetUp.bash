#!/bin/bash
kubectl create service clusterip service-am-i-ready --tcp=80:80 --dry-run=client -o yaml | kubectl apply -f -
kubectl patch svc service-am-i-ready -p '{"spec":{"selector":{"id":"cross-server-ready"}}}'
echo "Lab Setup Complete"
