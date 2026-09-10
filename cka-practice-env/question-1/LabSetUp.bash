#!/bin/bash
kubectl create namespace lima-control --dry-run=client -o yaml | kubectl apply -f -
kubectl create namespace lima-workload --dry-run=client -o yaml | kubectl apply -f -

kubectl create configmap config -n lima-control --from-literal=DNS_1=TODO --from-literal=DNS_2=TODO --from-literal=DNS_3=TODO --from-literal=DNS_4=TODO --dry-run=client -o yaml | kubectl apply -f -

kubectl create deployment controller --image=nginx -n lima-control --dry-run=client -o yaml | kubectl apply -f -

kubectl create service clusterip department --tcp=80:80 -n lima-workload --clusterip="None" --dry-run=client -o yaml | kubectl apply -f -
kubectl run section100 --image=nginx -n lima-workload --dry-run=client -o yaml | kubectl apply -f -

echo "Lab Setup Complete"
