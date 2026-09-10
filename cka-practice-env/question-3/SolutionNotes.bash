#!/bin/bash
# 1. ssh cka5248-node1
# 2. Check /var/lib/kubelet/pki/kubelet-client-current.pem
# 3. openssl x509 -in /var/lib/kubelet/pki/kubelet-client-current.pem -text | grep -i 'issuer\|extended'
# 4. Write output to /course/3/certificate-info.txt
