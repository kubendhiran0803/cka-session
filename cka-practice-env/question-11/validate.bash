#!/bin/bash
if kubectl get pod secret-pod -n secret > /dev/null 2>&1; then echo "[PASS] Pod created"; else echo "[FAIL] Pod missing"; fi
