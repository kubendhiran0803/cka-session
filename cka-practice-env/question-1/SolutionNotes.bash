#!/bin/bash
# DNS_1: kubernetes.default.svc.cluster.local
# DNS_2: department.lima-workload.svc.cluster.local
# DNS_3: 1-2-3-4.lima-workload.pod.cluster.local (replace IP with pod IP)
# DNS_4: 1-2-3-4.kube-system.pod.cluster.local

kubectl edit cm config -n lima-control
