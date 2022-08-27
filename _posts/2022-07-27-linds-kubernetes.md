---
layout: post
title: Moving to Kubernetes
tags: [kubernetes, homelab]
gh-repo: Jayden-Lind/LINDS-Kubernetes
---

# Introduction

I have been running multiple docker hosts with an assortment of containers that run random things. It was time to clean it up, define all the configurations, add some redundancy, and also allow easier upgrading/moving of the underlying OS.

## Setup

### Puppet Automation

To automate setting up of VM's, I implemented it through [Puppet](https://puppet.com/docs/puppet/7/install_puppet.html) and my manifests can be seen in [kubernetes.pp](https://github.com/Jayden-Lind/LINDS-Puppet/blob/master/manifests/kubernetes.pp), which uses [flannel](https://github.com/flannel-io/flannel) as the network fabric.

## Current deployment

My current deployment consists of:

1. [flannel](https://github.com/flannel-io/flannel)
2. [Ingress-NGINX](https://github.com/kubernetes/ingress-nginx)
3. [CSI-SMB Driver](https://github.com/kubernetes-csi/csi-driver-smb)
4. [My Kubernetes manifests](https://github.com/Jayden-Lind/LINDS-Kubernetes)
5. 2 x [TrueNAS](https://www.truenas.com/) hosts with 100GB storage with NFS being shared out to Kubernetes Pods.
6. [MetalLB](https://metallb.universe.tf/) to share other services using BGP and L2 advertisements.


![image](/img/2022/07/LINDS-Kubernetes.png)
