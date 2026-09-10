import os
import textwrap

base_dir = "cka-practice-env"
os.makedirs(base_dir, exist_ok=True)

questions = {
    1: {
        "desc": "Deployment DNS FQDNs",
        "question": textwrap.dedent("""\
            # Question 1
            # Solve this question on: ssh cka6016
            # 
            # The Deployment controller in Namespace lima-control communicates with various cluster-internal endpoints by using their DNS FQDN values.
            # 
            # Update the ConfigMap used by the Deployment with the correct FQDN values for:
            # 
            # 1. DNS_1 : Service kubernetes in Namespace default
            # 2. DNS_2 : Headless Service department in Namespace lima-workload
            # 3. DNS_3 : Pod section100 in Namespace lima-workload. It should work even if the Pod IP changes
            # 4. DNS_4 : A Pod with IP 1.2.3.4 in Namespace kube-system
            # 
            # Ensure the Deployment works with the updated values.
            # 
            # You can use nslookup or dig inside a Pod of the controller Deployment"""),
        "setup": textwrap.dedent("""\
            #!/bin/bash
            kubectl create namespace lima-control --dry-run=client -o yaml | kubectl apply -f -
            kubectl create namespace lima-workload --dry-run=client -o yaml | kubectl apply -f -
            
            kubectl create configmap config -n lima-control --from-literal=DNS_1=TODO --from-literal=DNS_2=TODO --from-literal=DNS_3=TODO --from-literal=DNS_4=TODO --dry-run=client -o yaml | kubectl apply -f -
            
            kubectl create deployment controller --image=nginx -n lima-control --dry-run=client -o yaml | kubectl apply -f -
            
            kubectl create service clusterip department --tcp=80:80 -n lima-workload --clusterip="None" --dry-run=client -o yaml | kubectl apply -f -
            kubectl run section100 --image=nginx -n lima-workload --dry-run=client -o yaml | kubectl apply -f -
            
            echo "Lab Setup Complete"
            """),
        "validate": textwrap.dedent("""\
            #!/bin/bash
            CM=$(kubectl get cm config -n lima-control -o yaml)
            
            if echo "$CM" | grep -q "DNS_1: kubernetes.default.svc.cluster.local"; then echo "[PASS] DNS_1 is correct"; else echo "[FAIL] DNS_1 is incorrect"; fi
            if echo "$CM" | grep -q "DNS_2: department.lima-workload.svc.cluster.local"; then echo "[PASS] DNS_2 is correct"; else echo "[FAIL] DNS_2 is incorrect"; fi
            """),
        "solution": textwrap.dedent("""\
            #!/bin/bash
            # DNS_1: kubernetes.default.svc.cluster.local
            # DNS_2: department.lima-workload.svc.cluster.local
            # DNS_3: 1-2-3-4.lima-workload.pod.cluster.local (replace IP with pod IP)
            # DNS_4: 1-2-3-4.kube-system.pod.cluster.local
            
            kubectl edit cm config -n lima-control
            """),
    },
    2: {
        "desc": "Static Pod NodePort",
        "question": textwrap.dedent("""\
            # Question 2
            # Solve this question on: ssh cka2560
            # 
            # Create a Static Pod named my-static-pod in Namespace default on the controlplane node. It should be of image nginx:1-alpine and have resource requests for 10m CPU and 20Mi memory.
            # 
            # Create a NodePort Service named static-pod-service which exposes that static Pod on port 80.
            # 
            # For verification check if the new Service has one Endpoint."""),
        "setup": textwrap.dedent("""\
            #!/bin/bash
            echo "Nothing to setup for Question 2. Proceed to solve."
            """),
        "validate": textwrap.dedent("""\
            #!/bin/bash
            if kubectl get pod my-static-pod-controlplane -n default > /dev/null 2>&1; then echo "[PASS] Static pod running"; else echo "[FAIL] Static pod not found"; fi
            if kubectl get svc static-pod-service -n default > /dev/null 2>&1; then echo "[PASS] Service created"; else echo "[FAIL] Service not found"; fi
            """),
        "solution": textwrap.dedent("""\
            #!/bin/bash
            # 1. ssh cka2560
            # 2. cd /etc/kubernetes/manifests
            # 3. kubectl run my-static-pod --image=nginx:1-alpine --dry-run=client -o yaml > my-static-pod.yaml
            # 4. Edit yaml to add resources: requests: cpu: 10m, memory: 20Mi
            # 5. kubectl expose pod my-static-pod-cka2560 --name static-pod-service --type=NodePort --port=80
            """),
    },
    3: {
        "desc": "TLS Bootstrapping",
        "question": textwrap.dedent("""\
            # Question 3
            # Solve this question on: ssh cka5248
            # 
            # Node cka5248-node1 has been added to the cluster using kubeadm and TLS bootstrapping.
            # 
            # Find the Issuer and Extended Key Usage values on cka5248-node1 for:
            # 1. Kubelet Client Certificate, the one used for outgoing connections to the kube-apiserver
            # 2. Kubelet Server Certificate, the one used for incoming connections from the kube-apiserver
            # 
            # Write the information into file /course/3/certificate-info.txt"""),
        "setup": textwrap.dedent("""\
            #!/bin/bash
            mkdir -p /course/3
            echo "Lab Setup Complete"
            """),
        "validate": textwrap.dedent("""\
            #!/bin/bash
            if [ -f /course/3/certificate-info.txt ]; then echo "[PASS] File exists"; else echo "[FAIL] File missing"; fi
            """),
        "solution": textwrap.dedent("""\
            #!/bin/bash
            # 1. ssh cka5248-node1
            # 2. Check /var/lib/kubelet/pki/kubelet-client-current.pem
            # 3. openssl x509 -in /var/lib/kubelet/pki/kubelet-client-current.pem -text | grep -i 'issuer\|extended'
            # 4. Write output to /course/3/certificate-info.txt
            """),
    },
    4: {
        "desc": "Probes",
        "question": textwrap.dedent("""\
            # Question 4
            # Do the following in Namespace default:
            # - Create a Pod named ready-if-service-ready of image nginx:1-alpine
            # - Configure a LivenessProbe which simply executes command true
            # - Configure a ReadinessProbe which checks if the url http://service-am-i-ready:80 is reachable. You can use wget -T2 -O- http://service-am-i-ready:80 for this.
            # - Start the Pod and confirm it isn't ready because of the ReadinessProbe.
            # Then:
            # - Create a second Pod named am-i-ready of image nginx:1-alpine with label id: cross-server-ready
            # - The already existing Service service-am-i-ready should now have that second Pod as endpoint.
            # - Now the first Pod should be in ready state, check that."""),
        "setup": textwrap.dedent("""\
            #!/bin/bash
            kubectl create service clusterip service-am-i-ready --tcp=80:80 --dry-run=client -o yaml | kubectl apply -f -
            kubectl patch svc service-am-i-ready -p '{"spec":{"selector":{"id":"cross-server-ready"}}}'
            echo "Lab Setup Complete"
            """),
        "validate": textwrap.dedent("""\
            #!/bin/bash
            if kubectl get pod ready-if-service-ready | grep -q "1/1"; then echo "[PASS] First pod is ready"; else echo "[FAIL] First pod is not ready"; fi
            """),
        "solution": textwrap.dedent("""\
            #!/bin/bash
            # Create pod with probes
            # livenessProbe:
            #   exec:
            #     command: ["true"]
            # readinessProbe:
            #   exec:
            #     command: ["wget", "-T2", "-O-", "http://service-am-i-ready:80"]
            """),
    },
    5: {
        "desc": "Kubectl Sorting",
        "question": textwrap.dedent("""\
            # Question 5
            # Create two bash script files which use kubectl sorting to:
            # 1. Write a command into /course/5/find_pods.sh which lists all Pods in all Namespaces sorted by their AGE (metadata.creationTimestamp)
            # 2. Write a command into /course/5/find_pods_uid.sh which lists all Pods in all Namespaces sorted by field metadata.uid"""),
        "setup": textwrap.dedent("""\
            #!/bin/bash
            mkdir -p /course/5
            echo "Lab Setup Complete"
            """),
        "validate": textwrap.dedent("""\
            #!/bin/bash
            if grep -q "sort-by=.metadata.creationTimestamp" /course/5/find_pods.sh; then echo "[PASS] find_pods.sh correct"; else echo "[FAIL] find_pods.sh incorrect"; fi
            if grep -q "sort-by=.metadata.uid" /course/5/find_pods_uid.sh; then echo "[PASS] find_pods_uid.sh correct"; else echo "[FAIL] find_pods_uid.sh incorrect"; fi
            """),
        "solution": textwrap.dedent("""\
            #!/bin/bash
            # echo "kubectl get pods -A --sort-by=.metadata.creationTimestamp" > /course/5/find_pods.sh
            # echo "kubectl get pods -A --sort-by=.metadata.uid" > /course/5/find_pods_uid.sh
            """),
    },
    6: {
        "desc": "Troubleshooting Kubelet",
        "question": textwrap.dedent("""\
            # Question 6
            # There seems to be an issue with the kubelet on controlplane node cka1024. It's not running.
            # Fix the kubelet and confirm that the node is available in Ready state.
            # Create a Pod called success in default Namespace of image nginx:1-alpine."""),
        "setup": textwrap.dedent("""\
            #!/bin/bash
            # Simulating broken kubelet on test node
            echo "In real lab, kubelet binary or service file is usually broken (e.g. wrong path or port)."
            """),
        "validate": textwrap.dedent("""\
            #!/bin/bash
            if kubectl get nodes | grep cka1024 | grep -q "Ready"; then echo "[PASS] Node is ready"; else echo "[FAIL] Node not ready"; fi
            if kubectl get pod success > /dev/null 2>&1; then echo "[PASS] Pod created"; else echo "[FAIL] Pod missing"; fi
            """),
        "solution": textwrap.dedent("""\
            #!/bin/bash
            # 1. systemctl status kubelet
            # 2. journalctl -u kubelet
            # 3. check /var/lib/kubelet/config.yaml or /etc/systemd/system/kubelet.service.d/10-kubeadm.conf
            # 4. Fix issue and systemctl daemon-reload && systemctl restart kubelet
            """),
    },
    7: {
        "desc": "etcd Backup",
        "question": textwrap.dedent("""\
            # Question 7
            # You have been tasked to perform the following etcd operations:
            # 1. Run etcd --version and store the output at /course/7/etcd-version
            # 2. Make a snapshot of etcd and save it at /course/7/etcd-snapshot.db"""),
        "setup": textwrap.dedent("""\
            #!/bin/bash
            mkdir -p /course/7
            """),
        "validate": textwrap.dedent("""\
            #!/bin/bash
            if [ -f /course/7/etcd-version ]; then echo "[PASS] etcd-version exists"; else echo "[FAIL] etcd-version missing"; fi
            if [ -f /course/7/etcd-snapshot.db ]; then echo "[PASS] snapshot exists"; else echo "[FAIL] snapshot missing"; fi
            """),
        "solution": textwrap.dedent("""\
            #!/bin/bash
            # ETCDCTL_API=3 etcdctl --version > /course/7/etcd-version
            # ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379 --cacert=/etc/kubernetes/pki/etcd/ca.crt --cert=/etc/kubernetes/pki/etcd/server.crt --key=/etc/kubernetes/pki/etcd/server.key snapshot save /course/7/etcd-snapshot.db
            """),
    },
    8: {
        "desc": "Controlplane Components",
        "question": textwrap.dedent("""\
            # Question 8
            # Check how the controlplane components kubelet, kube-apiserver, kube-scheduler, kube-controller-manager and etcd are started/installed on the controlplane node.
            # Also find out the name of the DNS application and how it's started/installed in the cluster.
            # Write your findings into file /course/8/controlplane-components.txt."""),
        "setup": textwrap.dedent("""\
            #!/bin/bash
            mkdir -p /course/8
            """),
        "validate": textwrap.dedent("""\
            #!/bin/bash
            if [ -f /course/8/controlplane-components.txt ]; then echo "[PASS] File exists"; else echo "[FAIL] File missing"; fi
            """),
        "solution": textwrap.dedent("""\
            #!/bin/bash
            # kubelet: process
            # kube-apiserver: static-pod
            # kube-scheduler: static-pod
            # kube-controller-manager: static-pod
            # etcd: static-pod
            # dns: pod CoreDNS
            """),
    },
    9: {
        "desc": "Manual Scheduling",
        "question": textwrap.dedent("""\
            # Question 9
            # Temporarily stop the kube-scheduler in a way that lets you start it again afterwards.
            # Create a single Pod named manual-schedule of image httpd:2-alpine, confirm it's created but not scheduled on any node.
            # Now you're the scheduler, manually schedule that Pod on node cka5248. Make sure it's running.
            # Start the kube-scheduler again and confirm it's running correctly by creating a second Pod named manual-schedule2..."""),
        "setup": textwrap.dedent("""\
            #!/bin/bash
            echo "Move /etc/kubernetes/manifests/kube-scheduler.yaml to /root/ to stop scheduler"
            """),
        "validate": textwrap.dedent("""\
            #!/bin/bash
            if kubectl get pod manual-schedule | grep -q "Running"; then echo "[PASS] Pod 1 running"; else echo "[FAIL] Pod 1 not running"; fi
            if kubectl get pod manual-schedule2 | grep -q "Running"; then echo "[PASS] Pod 2 running"; else echo "[FAIL] Pod 2 not running"; fi
            """),
        "solution": textwrap.dedent("""\
            #!/bin/bash
            # mv /etc/kubernetes/manifests/kube-scheduler.yaml /root/
            # create pod yaml, add nodeName: cka5248 under spec
            # mv /root/kube-scheduler.yaml /etc/kubernetes/manifests/
            """),
    },
    10: {
        "desc": "Dynamic Volume Provisioning",
        "question": textwrap.dedent("""\
            # Question 10
            # There is a backup Job which needs to be adjusted to use a PVC to store backups.
            # Create a StorageClass named local-backup which uses provisioner: rancher.io/local-path and volumeBindingMode: WaitForFirstConsumer.
            # The StorageClass should keep a PV retained even if a bound PVC is deleted.
            # Adjust the Job at /course/10/backup.yaml to use a PVC which requests 50Mi storage and uses the new StorageClass."""),
        "setup": textwrap.dedent("""\
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
            """),
        "validate": textwrap.dedent("""\
            #!/bin/bash
            if kubectl get sc local-backup > /dev/null 2>&1; then echo "[PASS] StorageClass created"; else echo "[FAIL] StorageClass missing"; fi
            if kubectl get job backup | grep -q "1/1"; then echo "[PASS] Job completed"; else echo "[FAIL] Job not completed"; fi
            """),
        "solution": textwrap.dedent("""\
            #!/bin/bash
            # Create SC with reclaimPolicy: Retain
            # Create PVC requesting 50Mi with storageClassName: local-backup
            # Modify job to add volumes and volumeMounts
            """),
    },
    11: {
        "desc": "Secrets Distribution",
        "question": textwrap.dedent("""\
            # Question 11
            # Create Namespace secret and implement the following in it:
            # - Create Pod secret-pod with image busybox:1. kept running by sleep 1d
            # - Create the existing Secret /course/11/secret1.yaml and mount it read-only into the Pod at /tmp/secret1
            # - Create a new Secret called secret2 which should contain user=user1 and pass=1234. These entries should be available inside the Pod as env vars APP_USER and APP_PASS"""),
        "setup": textwrap.dedent("""\
            #!/bin/bash
            mkdir -p /course/11
            kubectl create namespace secret --dry-run=client -o yaml | kubectl apply -f -
            cat <<EOF > /course/11/secret1.yaml
            apiVersion: v1
            kind: Secret
            metadata:
              name: secret1
              namespace: secret
            type: Opaque
            data:
              key: dGVzdAo=
            EOF
            """),
        "validate": textwrap.dedent("""\
            #!/bin/bash
            if kubectl get pod secret-pod -n secret > /dev/null 2>&1; then echo "[PASS] Pod created"; else echo "[FAIL] Pod missing"; fi
            """),
        "solution": textwrap.dedent("""\
            #!/bin/bash
            # kubectl apply -f /course/11/secret1.yaml
            # kubectl create secret generic secret2 --from-literal=user=user1 --from-literal=pass=1234 -n secret
            # edit pod to include volumeMounts and envFrom or env
            """),
    },
    13: {
        "desc": "Shared Volumes",
        "question": textwrap.dedent("""\
            # Question 13
            # Create a Pod with multiple containers named multi-container-playground in Namespace default:
            # - It should have a volume attached and mounted into each container.
            # - Container c1 with image nginx:1-alpine, name of the node should be available as env var MY_NODE_NAME
            # - Container c2 with image busybox:1 should write date to date.log in shared volume
            # - Container c3 with image busybox:1 should tail -f date.log from shared volume to stdout"""),
        "setup": textwrap.dedent("""\
            #!/bin/bash
            echo "No setup needed"
            """),
        "validate": textwrap.dedent("""\
            #!/bin/bash
            if kubectl get pod multi-container-playground > /dev/null 2>&1; then echo "[PASS] Pod created"; else echo "[FAIL] Pod missing"; fi
            """),
        "solution": textwrap.dedent("""\
            #!/bin/bash
            # Use emptyDir volume
            # For c1: env: valueFrom: fieldRef: fieldPath: spec.nodeName
            """),
    },
    14: {
        "desc": "Cluster Networking Info",
        "question": textwrap.dedent("""\
            # Question 14
            # You're asked to find out the following information about the cluster:
            # 1. How many controlplane nodes are available?
            # 2. How many worker nodes (non controlplane nodes) are available?
            # 3. What is the Service CIDR?
            # 4. Which Networking (or CNI Plugin) is configured and where is its config file?
            # 5. Which suffix will static pods have that run on cka8448?
            # Write your answers into file /course/14/cluster-info"""),
        "setup": textwrap.dedent("""\
            #!/bin/bash
            mkdir -p /course/14
            """),
        "validate": textwrap.dedent("""\
            #!/bin/bash
            if [ -f /course/14/cluster-info ]; then echo "[PASS] File exists"; else echo "[FAIL] File missing"; fi
            """),
        "solution": textwrap.dedent("""\
            #!/bin/bash
            # 1/2: kubectl get nodes
            # 3: cat /etc/kubernetes/manifests/kube-apiserver.yaml | grep service-cluster-ip-range
            # 4: ls /etc/cni/net.d/
            # 5: -cka8448
            """),
    },
    15: {
        "desc": "Cluster Events & Containerd",
        "question": textwrap.dedent("""\
            # Question 15
            # 1. Write a kubectl command into /course/15/cluster_events.sh which shows the latest events in the whole cluster, ordered by time.
            # 2. Delete the kube-proxy Pod and write the events this caused into /course/15/pod_kill.log
            # 3. Manually kill the containerd container of the kube-proxy Pod and write the events into /course/15/container_kill.log"""),
        "setup": textwrap.dedent("""\
            #!/bin/bash
            mkdir -p /course/15
            """),
        "validate": textwrap.dedent("""\
            #!/bin/bash
            if [ -f /course/15/cluster_events.sh ]; then echo "[PASS] File 1 exists"; else echo "[FAIL] File 1 missing"; fi
            """),
        "solution": textwrap.dedent("""\
            #!/bin/bash
            # 1: kubectl get events -A --sort-by=.metadata.creationTimestamp > /course/15/cluster_events.sh
            # 2: kubectl delete pod -n kube-system -l k8s-app=kube-proxy
            # 3: crictl ps | grep kube-proxy | crictl rm ...
            """),
    },
    16: {
        "desc": "Namespaced Resources & Roles",
        "question": textwrap.dedent("""\
            # Question 16
            # Write the names of all namespaced Kubernetes resources (like Pod, Secret, ConfigMap...) into /course/16/resources.txt.
            # Find the project-* Namespace with the highest number of Roles defined in it and write its name and amount of Roles into /course/16/crowded-namespace.txt."""),
        "setup": textwrap.dedent("""\
            #!/bin/bash
            mkdir -p /course/16
            kubectl create namespace project-a --dry-run=client -o yaml | kubectl apply -f -
            kubectl create namespace project-b --dry-run=client -o yaml | kubectl apply -f -
            kubectl create role r1 --verb=get --resource=pods -n project-a --dry-run=client -o yaml | kubectl apply -f -
            kubectl create role r2 --verb=get --resource=pods -n project-b --dry-run=client -o yaml | kubectl apply -f -
            kubectl create role r3 --verb=get --resource=pods -n project-b --dry-run=client -o yaml | kubectl apply -f -
            """),
        "validate": textwrap.dedent("""\
            #!/bin/bash
            if [ -f /course/16/resources.txt ]; then echo "[PASS] File exists"; else echo "[FAIL] File missing"; fi
            """),
        "solution": textwrap.dedent("""\
            #!/bin/bash
            # 1: kubectl api-resources --namespaced=true -o name > /course/16/resources.txt
            # 2: kubectl get roles -A | grep project-
            """),
    },
    17: {
        "desc": "Kustomize & RBAC",
        "question": textwrap.dedent("""\
            # Question 17
            # There is Kustomize config available at /course/17/operator.
            # Perform the following changes in the Kustomize base config:
            # 1. The operator needs to list certain CRDs. Check the logs to find out which ones and adjust permissions for Role operator-role.
            # 2. Add a new Student resource called student4 with any name and description.
            # Deploy your Kustomize config changes to prod."""),
        "setup": textwrap.dedent("""\
            #!/bin/bash
            mkdir -p /course/17/operator/base /course/17/operator/prod
            cat <<EOF > /course/17/operator/base/kustomization.yaml
            resources:
            - role.yaml
            EOF
            cat <<EOF > /course/17/operator/base/role.yaml
            apiVersion: rbac.authorization.k8s.io/v1
            kind: Role
            metadata:
              name: operator-role
              namespace: default
            rules: []
            EOF
            cat <<EOF > /course/17/operator/prod/kustomization.yaml
            resources:
            - ../base
            EOF
            """),
        "validate": textwrap.dedent("""\
            #!/bin/bash
            if kubectl get role operator-role > /dev/null 2>&1; then echo "[PASS] Role applied"; else echo "[FAIL] Role missing"; fi
            """),
        "solution": textwrap.dedent("""\
            #!/bin/bash
            # modify /course/17/operator/base/role.yaml to add permissions
            # add student4.yaml to base/kustomization.yaml
            # kubectl apply -k /course/17/operator/prod
            """),
    }
}

for q_num, q_data in questions.items():
    q_dir = os.path.join(base_dir, f"question-{q_num}")
    os.makedirs(q_dir, exist_ok=True)
    
    with open(os.path.join(q_dir, "LabSetUp.bash"), "w") as f:
        f.write(q_data["setup"].replace('\\n', '\n'))
    
    with open(os.path.join(q_dir, "Questions.bash"), "w") as f:
        f.write(q_data["question"].replace('\\n', '\n') + "\n")
        
    with open(os.path.join(q_dir, "validate.bash"), "w") as f:
        f.write(q_data["validate"].replace('\\n', '\n'))
        
    with open(os.path.join(q_dir, "SolutionNotes.bash"), "w") as f:
        f.write(q_data["solution"].replace('\\n', '\n'))
        
    with open(os.path.join(q_dir, "cleanup.bash"), "w") as f:
        f.write("#!/bin/bash\n# Add cleanup commands here\necho 'Cleanup complete'\n")

print("Generated all files successfully.")
