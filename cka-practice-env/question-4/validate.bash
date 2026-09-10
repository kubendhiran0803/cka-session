#!/bin/bash
if kubectl get pod ready-if-service-ready | grep -q "1/1"; then echo "[PASS] First pod is ready"; else echo "[FAIL] First pod is not ready"; fi
