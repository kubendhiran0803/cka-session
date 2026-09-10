#!/bin/bash
CM=$(kubectl get cm config -n lima-control -o yaml)

if echo "$CM" | grep -q "DNS_1: kubernetes.default.svc.cluster.local"; then echo "[PASS] DNS_1 is correct"; else echo "[FAIL] DNS_1 is incorrect"; fi
if echo "$CM" | grep -q "DNS_2: department.lima-workload.svc.cluster.local"; then echo "[PASS] DNS_2 is correct"; else echo "[FAIL] DNS_2 is incorrect"; fi
