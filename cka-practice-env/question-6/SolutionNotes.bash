#!/bin/bash
# 1. systemctl status kubelet
# 2. journalctl -u kubelet
# 3. check /var/lib/kubelet/config.yaml or /etc/systemd/system/kubelet.service.d/10-kubeadm.conf
# 4. Fix issue and systemctl daemon-reload && systemctl restart kubelet
