#!/bin/bash
if [ -f /course/7/etcd-version ]; then echo "[PASS] etcd-version exists"; else echo "[FAIL] etcd-version missing"; fi
if [ -f /course/7/etcd-snapshot.db ]; then echo "[PASS] snapshot exists"; else echo "[FAIL] snapshot missing"; fi
