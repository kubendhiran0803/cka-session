#!/bin/bash
if kubectl get pod my-static-pod-controlplane -n default > /dev/null 2>&1; then echo "[PASS] Static pod running"; else echo "[FAIL] Static pod not found"; fi
if kubectl get svc static-pod-service -n default > /dev/null 2>&1; then echo "[PASS] Service created"; else echo "[FAIL] Service not found"; fi
