#!/bin/bash
if kubectl get pod manual-schedule | grep -q "Running"; then echo "[PASS] Pod 1 running"; else echo "[FAIL] Pod 1 not running"; fi
if kubectl get pod manual-schedule2 | grep -q "Running"; then echo "[PASS] Pod 2 running"; else echo "[FAIL] Pod 2 not running"; fi
