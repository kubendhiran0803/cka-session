#!/bin/bash
# 1: kubectl get events -A --sort-by=.metadata.creationTimestamp > /course/15/cluster_events.sh
# 2: kubectl delete pod -n kube-system -l k8s-app=kube-proxy
# 3: crictl ps | grep kube-proxy | crictl rm ...
