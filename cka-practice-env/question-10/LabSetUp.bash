#!/bin/bash
mkdir -p /course/10
cat <<EOF > /course/10/backup.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: backup
spec:
  template:
    spec:
      containers:
      - name: backup
        image: busybox
        command: ["/bin/sh", "-c", "echo backup > /backup/backup.txt"]
      restartPolicy: Never
EOF
