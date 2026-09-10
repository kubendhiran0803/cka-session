#!/bin/bash
if grep -q "sort-by=.metadata.creationTimestamp" /course/5/find_pods.sh; then echo "[PASS] find_pods.sh correct"; else echo "[FAIL] find_pods.sh incorrect"; fi
if grep -q "sort-by=.metadata.uid" /course/5/find_pods_uid.sh; then echo "[PASS] find_pods_uid.sh correct"; else echo "[FAIL] find_pods_uid.sh incorrect"; fi
