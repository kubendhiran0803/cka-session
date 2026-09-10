#!/bin/bash
if kubectl get sc local-backup > /dev/null 2>&1; then echo "[PASS] StorageClass created"; else echo "[FAIL] StorageClass missing"; fi
if kubectl get job backup | grep -q "1/1"; then echo "[PASS] Job completed"; else echo "[FAIL] Job not completed"; fi
