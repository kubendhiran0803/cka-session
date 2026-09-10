#!/bin/bash
if kubectl get nodes | grep cka1024 | grep -q "Ready"; then echo "[PASS] Node is ready"; else echo "[FAIL] Node not ready"; fi
if kubectl get pod success > /dev/null 2>&1; then echo "[PASS] Pod created"; else echo "[FAIL] Pod missing"; fi
