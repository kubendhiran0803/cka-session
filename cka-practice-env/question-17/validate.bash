#!/bin/bash
if kubectl get role operator-role > /dev/null 2>&1; then echo "[PASS] Role applied"; else echo "[FAIL] Role missing"; fi
