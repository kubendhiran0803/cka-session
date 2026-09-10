#!/bin/bash
mkdir -p /course/16
kubectl create namespace project-a --dry-run=client -o yaml | kubectl apply -f -
kubectl create namespace project-b --dry-run=client -o yaml | kubectl apply -f -
kubectl create role r1 --verb=get --resource=pods -n project-a --dry-run=client -o yaml | kubectl apply -f -
kubectl create role r2 --verb=get --resource=pods -n project-b --dry-run=client -o yaml | kubectl apply -f -
kubectl create role r3 --verb=get --resource=pods -n project-b --dry-run=client -o yaml | kubectl apply -f -
