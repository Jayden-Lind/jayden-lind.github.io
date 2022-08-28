---
layout: post
title: Moving to Kubernetes
tags: [kubernetes, homelab]
gh-repo: Jayden-Lind/LINDS-Kubernetes
---

# Introduction

I have been running multiple Docker hosts with an assortment of containers that run random things. It was time to clean it up, define all the infrastructure, configurations, add some redundancy, and also allow easier upgrading/moving of the underlying OS.

## Setup

### Puppet Automation

To automate onboarding of a VM to the kubernetes cluster, I implemented it through [Puppet](https://puppet.com/docs/puppet/7/install_puppet.html) and my manifests can be seen in [kubernetes.pp](https://github.com/Jayden-Lind/LINDS-Puppet/blob/master/manifests/kubernetes.pp), which uses [flannel](https://github.com/flannel-io/flannel) as the network fabric.

## Current deployment

My current deployment consists of:

1. [flannel](https://github.com/flannel-io/flannel) for the networking fabric.
2. [Ingress-NGINX](https://github.com/kubernetes/ingress-nginx) for setting up an ingress controller, using NGINX virtualhosts to host multiple services on a single host.
3. [CSI-SMB Driver](https://github.com/kubernetes-csi/csi-driver-smb) for mounting SMB shares.
4. [My Kubernetes manifests](https://github.com/Jayden-Lind/LINDS-Kubernetes)
5. 2 x [TrueNAS](https://www.truenas.com/) hosts with 100GB storage, shared out through NFS for Physical Volumes to be created in K8s.
6. [MetalLB](https://metallb.universe.tf/) to share load balancing services using BGP and L2 advertisements.


### MetalLB

[MetalLB](https://metallb.universe.tf/) allows you to run a Kubernetes load balancer on bare metal hardware, compared to Cloud supplied load balancer.

I have this running in L2 (Layer 2) and BGP (Border Gateway Protocol) to learn and expirement with BGP.

From [metallb.yml](https://github.com/Jayden-Lind/LINDS-Kubernetes/blob/master/metallb.yml), I have set up the below.

```
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
  name: jd-bgp-pool
  namespace: metallb-system
spec:
  addresses:
  - 172.16.10.1-172.16.10.254
  - 172.16.11.1-172.16.11.254
---
apiVersion: metallb.io/v1beta1
kind: BGPAdvertisement
metadata:
  name: jd-bgp-advertisement
  namespace: metallb-system
spec:
  ipAddressPools:
  - jd-bgp-pool
---
apiVersion: metallb.io/v1beta2
kind: BGPPeer
metadata:
  name: jd-bgp-peer
  namespace: metallb-system
spec:
  myASN: 64500
  peerASN: 64550
  peerAddress: 10.0.50.1
```

IP pool to be advertised through BGP, and the BGP peer, which is my OPNSense box.

To confirm that a service is being advertised, I moved my Factorio server to use the BGP IP pool.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: factorio
  annotations:
    metallb.universe.tf/address-pool: jd-bgp-pool
  namespace: default
spec:
  type: LoadBalancer
  externalTrafficPolicy: Local
  selector:
    app: factorio
  ports:
...
```

Can confirm that the Factorio service is being advertised through kubectl

```shell
[root@jd-kube-01 LINDS-Kube]# kubectl get service factorio --namespace default 
NAME       TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)                           AGE
factorio   LoadBalancer   10.107.11.59   172.16.10.1   34197:31812/UDP,27015:31516/TCP   10d
[root@jd-kube-01 LINDS-Kube]# 
```

Now to confirm that from OPNsense we can see this 172.16.10.1 being advertised over BGP.

```shell
root@JD-OPNsense-01:~ # netstat -rn
Routing tables

Internet:
Destination        Gateway            Flags     Netif Expire
default            xxx.xxx.xxx.xxx    UGS        igb0
...
10.8.0.1           link#12            UH       ovpnc1
10.8.0.6           link#12            UHS         lo0
127.0.0.1          link#3             UH          lo0
172.16.10.1        10.0.53.8          UGH1   vmx0_vla
...
```

And we can see that the `factorio` service is now advertised through BGP from 10.0.53.8 (JD-Kube-02), and is on the route table of OPNSense.

# Diagram

![image](/img/2022/07/LINDS-Kubernetes.png)
